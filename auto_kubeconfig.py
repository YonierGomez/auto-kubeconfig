#!/usr/bin/env python3
"""
Script para automatizar la creación del fichero ~/.kube/config
con todos los clusters EKS de múltiples profiles de AWS.
"""

import os
import subprocess
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


def get_aws_profiles() -> List[str]:
    """
    Obtiene la lista de profiles de AWS desde ~/.aws/config
    """
    aws_config_path = Path.home() / '.aws' / 'config'
    
    if not aws_config_path.exists():
        print(f"❌ No se encontró el archivo {aws_config_path}")
        return []
    
    profiles = []
    with open(aws_config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[profile '):
                profile_name = line.replace('[profile ', '').replace(']', '')
                profiles.append(profile_name)
            elif line == '[default]':
                profiles.append('default')
    
    return profiles


def get_eks_clusters(profile: str) -> List[Dict[str, str]]:
    """
    Lista todos los clusters EKS para un profile y región específicos.
    Intenta obtener la región del profile, si no usa us-east-1 por defecto.
    """
    # Obtener la región del profile
    region = 'us-east-1'
    try:
        # Leer directamente del archivo de configuración
        aws_config_path = Path.home() / '.aws' / 'config'
        if aws_config_path.exists():
            with open(aws_config_path, 'r') as f:
                in_profile = False
                section_name = f'[profile {profile}]' if profile != 'default' else '[default]'
                
                for line in f:
                    line = line.strip()
                    if line == section_name:
                        in_profile = True
                    elif line.startswith('['):
                        in_profile = False
                    elif in_profile and line.startswith('region'):
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            region = parts[1].strip()
                            break
    except Exception:
        pass
    
    clusters = []
    
    # Intentar listar clusters en la región
    try:
        cmd = [
            'aws', 'eks', 'list-clusters',
            '--profile', profile,
            '--region', region,
            '--output', 'json'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            cluster_names = data.get('clusters', [])
            
            for cluster_name in cluster_names:
                clusters.append({
                    'name': cluster_name,
                    'region': region
                })
        else:
            # Silenciar errores de acceso, solo mostrar si hay problemas graves
            stderr = result.stderr.lower()
            if 'expired' in stderr or 'credentials' in stderr or 'token' in stderr:
                print(f"⚠️  Sesión expirada o sin credenciales para '{profile}'. Ejecuta: aws sso login --profile {profile}")
            
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timeout al listar clusters para profile '{profile}'")
    except Exception as e:
        pass  # Silenciar otros errores
    
    return clusters


def get_kubeconfig_for_cluster(profile: str, cluster_name: str, region: str) -> Dict[str, Any]:
    """
    Obtiene la configuración de kubeconfig para un cluster específico.
    """
    try:
        cmd = [
            'aws', 'eks', 'describe-cluster',
            '--name', cluster_name,
            '--profile', profile,
            '--region', region,
            '--output', 'json'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            cluster_info = data.get('cluster', {})
            
            cluster_arn = cluster_info.get('arn', '')
            endpoint = cluster_info.get('endpoint', '')
            ca_data = cluster_info.get('certificateAuthority', {}).get('data', '')
            
            return {
                'cluster_arn': cluster_arn,
                'endpoint': endpoint,
                'ca_data': ca_data,
                'name': cluster_name,
                'region': region,
                'profile': profile
            }
    except Exception as e:
        print(f"⚠️  Error al obtener info del cluster '{cluster_name}': {e}")
    
    return None


def generate_kubeconfig(clusters_info: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Genera la estructura completa del kubeconfig.
    """
    kubeconfig = {
        'apiVersion': 'v1',
        'kind': 'Config',
        'clusters': [],
        'contexts': [],
        'users': [],
        'current-context': ''
    }
    
    for info in clusters_info:
        if not info:
            continue
            
        cluster_arn = info['cluster_arn']
        cluster_name = info['name']
        endpoint = info['endpoint']
        ca_data = info['ca_data']
        region = info['region']
        profile = info['profile']
        
        # Añadir cluster
        kubeconfig['clusters'].append({
            'cluster': {
                'certificate-authority-data': ca_data,
                'server': endpoint
            },
            'name': cluster_arn
        })
        
        # Añadir user
        user_name = cluster_arn
        kubeconfig['users'].append({
            'name': user_name,
            'user': {
                'exec': {
                    'apiVersion': 'client.authentication.k8s.io/v1beta1',
                    'command': 'aws',
                    'args': [
                        '--region',
                        region,
                        'eks',
                        'get-token',
                        '--cluster-name',
                        cluster_name,
                        '--output',
                        'json'
                    ],
                    'env': [
                        {
                            'name': 'AWS_PROFILE',
                            'value': profile
                        }
                    ]
                }
            }
        })
        
        # Añadir context
        context_name = cluster_arn
        kubeconfig['contexts'].append({
            'context': {
                'cluster': cluster_arn,
                'user': user_name
            },
            'name': context_name
        })
    
    # Establecer el primer contexto como actual
    if kubeconfig['contexts']:
        kubeconfig['current-context'] = kubeconfig['contexts'][0]['name']
    
    return kubeconfig


def save_kubeconfig(kubeconfig: Dict[str, Any], output_path: Path, backup: bool = True):
    """
    Guarda el kubeconfig en el archivo especificado.
    """
    # Crear backup si el archivo existe
    if output_path.exists() and backup:
        backup_path = output_path.with_suffix('.backup')
        print(f"📦 Creando backup en: {backup_path}")
        import shutil
        shutil.copy2(output_path, backup_path)
    
    # Crear directorio si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar el archivo
    with open(output_path, 'w') as f:
        yaml.dump(kubeconfig, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Kubeconfig guardado en: {output_path}")


def process_profile(profile: str, index: int, total: int, verbose: bool) -> List[Dict[str, Any]]:
    """
    Procesa un profile y retorna la información de sus clusters.
    """
    clusters_info = []
    clusters = get_eks_clusters(profile)
    
    if clusters:
        for cluster in clusters:
            cluster_name = cluster['name']
            region = cluster['region']
            
            cluster_info = get_kubeconfig_for_cluster(profile, cluster_name, region)
            if cluster_info:
                clusters_info.append(cluster_info)
    
    return {
        'profile': profile,
        'clusters_info': clusters_info,
        'cluster_count': len(clusters)
    }


def main():
    parser = argparse.ArgumentParser(
        description='Automatiza la creación del fichero kubeconfig con todos los clusters EKS'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='~/.kube/config',
        help='Ruta del archivo de salida (default: ~/.kube/config)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='No crear backup del archivo existente'
    )
    parser.add_argument(
        '--profiles',
        type=str,
        nargs='+',
        help='Profiles específicos a procesar (default: todos)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostrar lo que se haría sin escribir el archivo'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada durante el proceso'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Modo silencioso, solo mostrar errores críticos'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=10,
        help='Número de workers paralelos para procesar profiles (default: 10)'
    )
    
    args = parser.parse_args()
    
    verbose = args.verbose
    quiet = args.quiet
    
    if not quiet:
        print("🚀 Iniciando generación automática de kubeconfig...\n")
    
    # Obtener profiles
    if args.profiles:
        profiles = args.profiles
        if verbose:
            print(f"📋 Usando profiles especificados: {', '.join(profiles)}")
    else:
        profiles = get_aws_profiles()
        if verbose:
            print(f"📋 Profiles encontrados: {len(profiles)} profiles")
        elif not quiet:
            print(f"📋 Encontrados {len(profiles)} profiles en ~/.aws/config")
    
    if not profiles:
        print("❌ No se encontraron profiles de AWS")
        sys.exit(1)
    
    if not quiet:
        print(f"\n🔍 Buscando clusters EKS...\n")
    
    # Recopilar información de todos los clusters usando procesamiento paralelo
    all_clusters_info = []
    profiles_with_clusters = 0
    print_lock = Lock()
    
    # Usar ThreadPoolExecutor para procesar profiles en paralelo
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Enviar todas las tareas
        future_to_profile = {
            executor.submit(process_profile, profile, i, len(profiles), verbose): profile
            for i, profile in enumerate(profiles)
        }
        
        completed = 0
        # Procesar resultados conforme se completan
        for future in as_completed(future_to_profile):
            profile = future_to_profile[future]
            completed += 1
            
            try:
                result = future.result()
                
                if result['clusters_info']:
                    profiles_with_clusters += 1
                    all_clusters_info.extend(result['clusters_info'])
                    
                    with print_lock:
                        if not quiet:
                            print(f"   ✓ [{completed}/{len(profiles)}] {result['profile']}: {result['cluster_count']} cluster(s)")
                elif verbose:
                    with print_lock:
                        print(f"   ⚠️  [{completed}/{len(profiles)}] {profile}: Sin clusters")
            except Exception as e:
                if verbose:
                    with print_lock:
                        print(f"   ❌ [{completed}/{len(profiles)}] {profile}: Error - {e}")
    
    if not quiet:
        print()
    
    if not all_clusters_info:
        print("❌ No se encontraron clusters EKS en ningún profile")
        print("💡 Asegúrate de:")
        print("   1. Haber iniciado sesión con: aws sso login --profile <profile>")
        print("   2. Tener permisos para listar clusters EKS")
        print("   3. Que existan clusters en las cuentas")
        sys.exit(1)
    
    if not quiet:
        print(f"✅ Encontrados {len(all_clusters_info)} cluster(s) en {profiles_with_clusters} profile(s)\n")
    
    # Generar kubeconfig
    if verbose:
        print("🔧 Generando kubeconfig...")
    kubeconfig = generate_kubeconfig(all_clusters_info)
    
    output_path = Path(args.output).expanduser()
    
    if args.dry_run:
        print("\n🔍 DRY RUN - Contenido que se generaría:\n")
        print(yaml.dump(kubeconfig, default_flow_style=False, sort_keys=False))
        print(f"\n📝 Se escribiría en: {output_path}")
    else:
        # Guardar kubeconfig
        save_kubeconfig(kubeconfig, output_path, backup=not args.no_backup)
        
        if not quiet:
            print(f"\n✨ Proceso completado exitosamente!")
            print(f"📊 Se configuraron {len(kubeconfig['clusters'])} clusters")
            print(f"📊 Se crearon {len(kubeconfig['contexts'])} contextos")
            print(f"\n💡 Puedes cambiar de contexto con: kubectl config use-context <nombre-contexto>")
            print(f"💡 Ver contextos disponibles: kubectl config get-contexts")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

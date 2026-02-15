# Ejemplos de Uso

Este documento contiene ejemplos detallados de cómo usar auto-kubeconfig en diferentes escenarios.

## 📋 Tabla de Contenidos

- [Uso Básico](#uso-básico)
- [Escenarios Comunes](#escenarios-comunes)
- [AWS SSO](#aws-sso)
- [Troubleshooting](#troubleshooting)

## Uso Básico

### Generar kubeconfig con todos los profiles

```bash
python auto_kubeconfig.py
```

Salida esperada:
```
🚀 Iniciando generación automática de kubeconfig...
📋 Encontrados 255 profiles en ~/.aws/config
🔍 Buscando clusters EKS...
   ✓ [5/255] profile1: 1 cluster(s)
   ✓ [10/255] profile2: 2 cluster(s)
...
✅ Encontrados 204 cluster(s) en 162 profile(s)
✅ Kubeconfig guardado en: /Users/user/.kube/config
```

### Ver qué se generaría sin modificar nada

```bash
python auto_kubeconfig.py --dry-run
```

Esto te mostrará el contenido completo del kubeconfig que se generaría.

## Escenarios Comunes

### 1. Solo procesar profiles de producción

```bash
python auto_kubeconfig.py --profiles prod-account1 prod-account2 prod-account3
```

### 2. Generar kubeconfig alternativo

```bash
python auto_kubeconfig.py --output ~/.kube/config-backup
```

### 3. Modo silencioso (solo errores)

```bash
python auto_kubeconfig.py --quiet
```

### 4. Modo verbose (máximo detalle)

```bash
python auto_kubeconfig.py --verbose
```

### 5. Sin crear backup

```bash
python auto_kubeconfig.py --no-backup
```

### 6. Ajustar workers paralelos

Para procesar más rápido (más carga de CPU):
```bash
python auto_kubeconfig.py --workers 20
```

Para procesar más lento (menos carga de CPU):
```bash
python auto_kubeconfig.py --workers 5
```

## AWS SSO

### Iniciar sesión con AWS SSO

Si tienes múltiples profiles con SSO, necesitas autenticarte:

```bash
# Iniciar sesión en un profile específico
aws sso login --profile my-profile

# O si usas una sesión SSO compartida
aws sso login --sso-session bco
```

### Verificar sesión SSO activa

```bash
aws sts get-caller-identity --profile my-profile
```

Si ves un error de token expirado, ejecuta nuevamente `aws sso login`.

### Configuración de AWS SSO

Tu `~/.aws/config` debe tener esta estructura:

```ini
[sso-session bco]
sso_start_url = https://your-id.awsapps.com/start/#
sso_region = us-east-1

[profile dev-account]
sso_session = bco
sso_account_id = 123456789012
sso_role_name = DeveloperRole
region = us-east-1
output = json

[profile prod-account]
sso_session = bco
sso_account_id = 987654321098
sso_role_name = AdminRole
region = us-east-1
output = json
```

## Uso con kubectl

### Ver todos los contextos

```bash
kubectl config get-contexts
```

### Ver solo nombres de contextos

```bash
kubectl config get-contexts -o name
```

### Buscar contextos específicos

```bash
# Buscar por nombre de cuenta
kubectl config get-contexts | grep dev

# Buscar por nombre de cluster
kubectl config get-contexts | grep eks-app
```

### Cambiar de contexto

```bash
kubectl config use-context arn:aws:eks:us-east-1:123456789012:cluster/my-cluster
```

### Ver contexto actual

```bash
kubectl config current-context
```

### Probar conexión al cluster

```bash
# Ver nodos
kubectl get nodes

# Ver pods en todos los namespaces
kubectl get pods -A

# Ver servicios
kubectl get svc -A
```

## Automatización

### Script para actualizar kubeconfig diariamente

Crea un script `update_kubeconfig.sh`:

```bash
#!/bin/bash
set -e

# Renovar sesión SSO
aws sso login --sso-session bco

# Actualizar kubeconfig
cd /path/to/auto-kubeconfig
python auto_kubeconfig.py --quiet

echo "✅ Kubeconfig actualizado: $(date)"
```

Hazlo ejecutable y agrégalo a cron:

```bash
chmod +x update_kubeconfig.sh

# Ejecutar diariamente a las 8am
crontab -e
# Agregar: 0 8 * * * /path/to/update_kubeconfig.sh >> /var/log/kubeconfig-update.log 2>&1
```

### Integración con CI/CD

Ejemplo para GitHub Actions:

```yaml
- name: Generate Kubeconfig
  run: |
    pip install -r requirements.txt
    python auto_kubeconfig.py --output $GITHUB_WORKSPACE/kubeconfig
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## Troubleshooting

### Error: "Token has expired"

**Solución:**
```bash
aws sso login --profile your-profile
# o
aws sso login --sso-session your-session
```

### Error: "No se encontraron clusters"

**Posibles causas:**
1. No tienes clusters en esas cuentas
2. No tienes permisos para listar clusters
3. La sesión SSO expiró

**Verificar permisos:**
```bash
aws eks list-clusters --profile your-profile
```

### Error: "No se encontraron profiles"

**Solución:**
Verifica que `~/.aws/config` existe y tiene profiles:
```bash
cat ~/.aws/config | grep "\[profile"
```

### El script es muy lento

**Soluciones:**
1. Aumentar workers: `--workers 20`
2. Procesar solo profiles necesarios: `--profiles prod1 prod2`
3. Verificar tu conexión a internet

### Error al conectar con kubectl

**Verificar:**
```bash
# 1. Verificar AWS CLI
aws --version

# 2. Verificar kubectl
kubectl version --client

# 3. Verificar sesión AWS
aws sts get-caller-identity --profile your-profile

# 4. Probar obtener token manualmente
aws eks get-token --cluster-name your-cluster --profile your-profile
```

## Tips y Mejores Prácticas

### 1. Mantén backups

Siempre que regeneres el kubeconfig, se crea un backup automático. Si algo sale mal:

```bash
cp ~/.kube/config.backup ~/.kube/config
```

### 2. Nombres de contextos largos

Los contextos usan ARNs completos. Para facilitar el uso, crea aliases:

```bash
# En tu .zshrc o .bashrc
alias k8s-dev='kubectl config use-context arn:aws:eks:us-east-1:123:cluster/dev'
alias k8s-prod='kubectl config use-context arn:aws:eks:us-east-1:456:cluster/prod'
```

### 3. Organizar múltiples kubeconfigs

Si tienes diferentes kubeconfigs para diferentes propósitos:

```bash
# Desarrollo
export KUBECONFIG=~/.kube/config-dev

# Producción (más cuidado!)
export KUBECONFIG=~/.kube/config-prod

# Combinar múltiples
export KUBECONFIG=~/.kube/config:~/.kube/config-dev:~/.kube/config-prod
```

### 4. Usar con kubectx/kubens

Instala [kubectx](https://github.com/ahmetb/kubectx) para cambiar contextos fácilmente:

```bash
# Instalar
brew install kubectx

# Cambiar de contexto
kubectx arn:aws:eks:us-east-1:123:cluster/dev

# Ver contextos con filtro
kubectx | grep dev
```

## Recursos Adicionales

- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [kubectl Documentation](https://kubernetes.io/docs/reference/kubectl/)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [AWS SSO Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)

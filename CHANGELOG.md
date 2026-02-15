# Changelog

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-02-15

### Added
- Generación automática de kubeconfig desde múltiples profiles AWS
- Soporte para AWS SSO
- Procesamiento paralelo con ThreadPoolExecutor (10 workers por defecto)
- Opciones de línea de comandos:
  - `--output`: Especificar ruta de salida
  - `--profiles`: Filtrar profiles específicos
  - `--dry-run`: Modo de prueba sin modificar archivos
  - `--verbose`: Modo detallado
  - `--quiet`: Modo silencioso
  - `--no-backup`: Deshabilitar backup automático
  - `--workers`: Configurar número de workers paralelos
- Backup automático del kubeconfig existente
- Detección automática de región por profile
- Autenticación dinámica con `aws eks get-token`
- Manejo de errores de sesión SSO expirada
- Script interactivo de ejemplo (`run_example.sh`)
- Documentación completa en README.md
- Archivo de requisitos (requirements.txt)

### Features
- Procesa 255+ profiles en 1-2 minutos
- Detecta y configura 200+ clusters EKS automáticamente
- Genera contextos de kubectl listos para usar
- Preserva configuración existente con backups

## [Unreleased]

### Planned
- Tests automatizados con pytest
- Soporte para múltiples regiones por profile
- Filtrado de clusters por tags
- Exportar configuración a diferentes formatos
- Integración con CI/CD
- Modo interactivo para seleccionar profiles
- Caché de resultados para acelerar ejecuciones repetidas
- Validación de acceso a clusters antes de agregar

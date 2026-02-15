auto-kubeconfig/
├── .github/                          # Configuración de GitHub
│   ├── workflows/                    # GitHub Actions
│   │   └── lint.yml                  # Workflow de linting
│   ├── ISSUE_TEMPLATE/               # Templates para issues
│   │   ├── bug_report.md            # Template de bug report
│   │   └── feature_request.md       # Template de feature request
│   └── pull_request_template.md     # Template de pull request
│
├── .editorconfig                     # Configuración de editor
├── .gitignore                        # Archivos ignorados por git
├── CHANGELOG.md                      # Historial de cambios
├── CONTRIBUTING.md                   # Guía de contribución
├── EXAMPLES.md                       # Ejemplos de uso detallados
├── LICENSE                           # Licencia MIT
├── Makefile                          # Comandos útiles de make
├── README.md                         # Documentación principal
├── auto_kubeconfig.py               # Script principal
├── requirements.txt                  # Dependencias Python
├── run_example.sh                   # Script interactivo de ejemplo
└── setup.py                         # Configuración de instalación

## Descripción de Archivos

### Archivos Principales

- **auto_kubeconfig.py**: Script principal que genera el kubeconfig
- **requirements.txt**: Lista de dependencias de Python (PyYAML)
- **setup.py**: Permite instalar el script como paquete Python

### Documentación

- **README.md**: Documentación principal con características y uso básico
- **EXAMPLES.md**: Ejemplos detallados de uso para diferentes escenarios
- **CONTRIBUTING.md**: Guía para contribuir al proyecto
- **CHANGELOG.md**: Historial de versiones y cambios
- **LICENSE**: Licencia MIT del proyecto

### Configuración

- **.gitignore**: Especifica qué archivos no deben ser versionados
- **.editorconfig**: Configuración de estilo de código para diferentes editores
- **Makefile**: Comandos convenientes (install, run, clean, etc.)

### Scripts Auxiliares

- **run_example.sh**: Script interactivo que guía en el uso del programa

### GitHub

- **.github/workflows/lint.yml**: GitHub Action para verificar calidad del código
- **.github/ISSUE_TEMPLATE/**: Templates para crear issues estructurados
- **.github/pull_request_template.md**: Template para pull requests

## Archivos Generados (No versionados)

Estos archivos se generan durante la ejecución pero no se incluyen en git:

- **config**: Archivo de ejemplo de kubeconfig (solo para referencia)
- **~/.kube/config**: Kubeconfig generado (ubicación predeterminada)
- **~/.kube/config.backup**: Backup automático del kubeconfig anterior
- **__pycache__/**: Cache de Python
- ***.pyc**: Bytecode compilado de Python
- **venv/**: Entorno virtual de Python

## Estructura Recomendada para Desarrollo

Si vas a desarrollar o extender el proyecto:

```
auto-kubeconfig/
├── .github/
├── docs/                            # Documentación adicional
│   ├── architecture.md              # Documentación de arquitectura
│   └── api.md                       # Documentación de API
├── tests/                           # Tests unitarios
│   ├── __init__.py
│   ├── test_aws_profiles.py
│   ├── test_kubeconfig_gen.py
│   └── fixtures/                    # Datos de prueba
├── examples/                        # Scripts de ejemplo adicionales
│   └── custom_filters.py
├── auto_kubeconfig.py
├── requirements.txt
├── requirements-dev.txt             # Dependencias de desarrollo
└── ...
```

## Flujo de Trabajo

1. **Desarrollo**: Modifica `auto_kubeconfig.py`
2. **Prueba local**: `make dry-run` o `python auto_kubeconfig.py --dry-run`
3. **Limpieza**: `make clean`
4. **Commit**: Sigue las guías en CONTRIBUTING.md
5. **Pull Request**: Usa el template en `.github/pull_request_template.md`
6. **CI/CD**: GitHub Actions ejecuta lint automáticamente

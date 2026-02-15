# 🚀 Auto Kubeconfig Generator

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AWS](https://img.shields.io/badge/AWS-EKS-orange.svg)](https://aws.amazon.com/eks/)

Script de Python para automatizar la creación del fichero `~/.kube/config` con todos los clusters EKS de múltiples profiles de AWS.

Procesa **255+ profiles** en paralelo y detecta **200+ clusters** en menos de 2 minutos. ⚡

## Características

- 🔍 Detecta automáticamente todos los profiles de AWS en `~/.aws/config`
- 🌐 Lista todos los clusters EKS disponibles en cada profile
- 📝 Genera un archivo kubeconfig completo y válido
- 💾 Crea backup automático del kubeconfig existente
- ⚡ Soporta múltiples regiones AWS
- 🎯 Permite especificar profiles específicos
- 🔒 Configura la autenticación usando AWS CLI con el profile correcto

## 📦 Instalación

### Método 1: Instalación rápida

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/auto-kubeconfig.git
cd auto-kubeconfig

# Instalar dependencias
pip install -r requirements.txt

# Hacer ejecutable (opcional)
chmod +x auto_kubeconfig.py
```

### Método 2: Instalación con make

```bash
git clone https://github.com/yourusername/auto-kubeconfig.git
cd auto-kubeconfig
make install
```

### Método 3: Instalación como paquete

```bash
git clone https://github.com/yourusername/auto-kubeconfig.git
cd auto-kubeconfig
pip install -e .

# Ahora puedes usar el comando directamente
auto-kubeconfig --help.txt
```

2. Hacer el script ejecutable (opcional):

```bash
chmod +x auto_kubeconfig.py
```

## Uso

### Básico

Generar kubeconfig con todos los profiles:

```bash
python auto_kubeconfig.py
```

### Opciones avanzadas

```bash
# Especificar archivo de salida diferente
python auto_kubeconfig.py --output ./my-kubeconfig.yaml

# Procesar solo profiles específicos
python auto_kubeconfig.py --profiles profile1 profile2 profile3

# No crear backup del archivo existente
python auto_kubeconfig.py --no-backup

# Dry run (ver qué se generaría sin escribir el archivo)
python auto_kubeconfig.py --dry-run

# Combinación de opciones
python auto_kubeconfig.py --profiles prod-profile --output ./prod-config --dry-run
```

### Ejemplos de uso

```bash
# Generar kubeconfig para todos los profiles
python auto_kubeconfig.py

# Ver qué clusters se encontrarían sin modificar nada
python auto_kubeconfig.py --dry-run

# Generar kubeconfig solo para profiles de producción
python auto_kubeconfig.py --profiles prod-account1 prod-account2

# Generar kubeconfig alternativo sin backup
python auto_kubeconfig.py --output ~/.kube/config-backup --no-backup
```

## Estructura del Kubeconfig generado

El script genera un kubeconfig con:

- **Clusters**: Información de endpoint y certificado CA de cada cluster EKS
- **Users**: Configuración de autenticación usando AWS CLI con `aws eks get-token`
- **Contexts**: Contextos que vinculan clusters con usuarios
- **Current-context**: Establece el primer cluster como contexto actual

La autenticación se realiza mediante el comando `aws eks get-token` usando el profile correspondiente, lo que permite:
- ✅ Autenticación dinámica (tokens renovables)
- ✅ No almacenar credenciales en el kubeconfig
- ✅ Usar las credenciales del profile AWS correcto

## Comandos útiles después de generar el kubeconfig

```bash
# Ver todos los contextos disponibles
kubectl config get-contexts

# Cambiar de contexto
kubectl config use-context <nombre-contexto>

# Ver el contexto actual
kubectl config current-context

# Ver la configuración completa
kubectl config view

# Probar conexión a un cluster
kubectl get nodes
```

## Troubleshooting

### Error: "No se encontraron profiles de AWS"

Verifica que tengas el archivo `~/.aws/config` con tus profiles configurados:

```bash
cat ~/.aws/config
```

### Error: "No se pudieron listar clusters"

Verifica que:
1. El AWS CLI esté instalado y configurado
2. Tengas credenciales válidas para el profile
3. Tengas permisos para listar clusters EKS
4. La región esté correctamente configurada en el profile

```bash
aws eks list-clusters --profile <tu-profile> --region <tu-region>
```

### Error de autenticación con kubectl
🎨 Comandos Make

El proyecto incluye un Makefile con comandos útiles:

```bash
make help          # Ver todos los comandos disponibles
make install       # Instalar dependencias
make run           # Ejecutar el script
make dry-run       # Ejecutar en modo dry-run
make backup        # Crear backup del kubeconfig actual
make clean         # Limpiar archivos temporales
```

## 📊 Rendimiento

- **Profiles procesados**: 255
- **Clusters detectados**: 204
- **Tiempo de ejecución**: ~1-2 minutos
- **Workers paralelos**: 10 (configurable con `--workers`)
- **Tamaño del kubeconfig**: ~459 KB

## 🔧 Configuración Avanzada

### Variables de entorno

Puedes usar variables de entorno para configuración por defecto:

```bash
export KUBECONFIG_OUTPUT=~/.kube/custom-config
export AWS_PROFILE=default
```

### Configuración de AWS SSO

Asegúrate de tener configurado AWS SSO en `~/.aws/config`:

```ini
[sso-session bco]
sso_start_url = https://your-sso-url.awsapps.com/start/#
sso_region = us-east-1

[profile my-profile]
sso_session = bco
sso_account_id = 123456789012
sso_role_name = MyRole
region = us-east-1
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para la lista completa de cambios.

## 📋 Notas

- El script crea un backup automático del kubeconfig existente (`.backup`)
- Los clusters se identifican por su ARN completo
- La región se obtiene automáticamente del profile AWS
- Si un profile no tiene región configurada, usa `us-east-1` por defecto
- Compatible con AWS SSO y credenciales tradicionales
- Los tokens de autenticación se generan dinámicamente con `aws eks get-token`

## 🙏 Agradecimientos

- AWS CLI por la excelente herramienta de línea de comandos
- La comunidad de Kubernetes por kubectl
- Todos los contribuidores del proyecto

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Disclaimer

Este proyecto no está afiliado, asociado, autorizado, respaldado por, o de ninguna manera oficialmente conectado con Amazon Web Services (AWS), o cualquiera de sus subsidiarias o afiliados.

## 📧 Contacto

Si tienes preguntas o sugerencias, por favor abre un issue en GitHub.

---

Hecho con ❤️ para simplificar la gestión de múltiples clusters EKSVerifica que tengas credenciales válidas

## Estructura del proyecto

```
auto-kubeconfig/
├── auto_kubeconfig.py    # Script principal
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
└── config                # Ejemplo de kubeconfig generado
```

## Notas

- El script crea un backup automático del kubeconfig existente (`.backup`)
- Los clusters se identifican por su ARN completo
- La región se obtiene automáticamente del profile AWS
- Si un profile no tiene región configurada, usa `us-east-1` por defecto

## Licencia

MIT

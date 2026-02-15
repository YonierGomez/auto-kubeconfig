# Contribuyendo a Auto Kubeconfig Generator

¡Gracias por tu interés en contribuir! Este documento proporciona pautas para contribuir al proyecto.

## 🚀 Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor abre un issue incluyendo:

- Descripción clara del problema
- Pasos para reproducir el bug
- Comportamiento esperado vs. comportamiento actual
- Versión de Python, AWS CLI y sistema operativo
- Logs o mensajes de error relevantes

### Sugerir Mejoras

Las sugerencias de mejoras son bienvenidas. Por favor:

- Describe claramente la mejora propuesta
- Explica por qué sería útil
- Proporciona ejemplos de uso si es posible

### Pull Requests

1. **Fork el repositorio** y crea tu rama desde `main`:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Haz tus cambios** siguiendo las guías de estilo:
   - Usa nombres descriptivos para variables y funciones
   - Agrega comentarios donde sea necesario
   - Mantén las líneas de código bajo 100 caracteres cuando sea posible

3. **Prueba tu código**:
   ```bash
   python auto_kubeconfig.py --dry-run
   ```

4. **Commit tus cambios**:
   ```bash
   git commit -m "feat: descripción clara del cambio"
   ```

   Usa prefijos en commits:
   - `feat:` para nuevas funcionalidades
   - `fix:` para correcciones de bugs
   - `docs:` para cambios en documentación
   - `style:` para cambios de formato
   - `refactor:` para refactorización de código
   - `test:` para agregar tests
   - `chore:` para tareas de mantenimiento

5. **Push a tu fork**:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

6. **Abre un Pull Request** desde GitHub

## 📝 Guías de Estilo

### Python

- Sigue PEP 8
- Usa type hints cuando sea posible
- Docstrings para funciones públicas
- Nombres descriptivos en inglés o español (consistente)

### Commits

- Usa el presente imperativo: "Agrega funcionalidad" no "Agregada funcionalidad"
- Primera línea: resumen conciso (máx. 72 caracteres)
- Líneas adicionales: descripción detallada si es necesario

## 🧪 Testing

Aunque actualmente no hay tests automatizados, es recomendable:

- Probar con diferentes configuraciones de AWS
- Verificar con múltiples profiles
- Probar con y sin clusters existentes
- Validar dry-run vs. ejecución real

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la Licencia MIT del proyecto.

## ❓ Preguntas

Si tienes preguntas, abre un issue con la etiqueta `question`.

¡Gracias por contribuir! 🎉

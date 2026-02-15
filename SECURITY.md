# Security Policy

## Versiones Soportadas

| Versión | Soportada          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reportar una Vulnerabilidad

La seguridad de este proyecto es importante. Si descubres una vulnerabilidad de seguridad, por favor repórtala de manera responsable.

### Cómo Reportar

**Por favor NO crees un issue público** para reportar vulnerabilidades de seguridad.

En su lugar:

1. **Email**: Envía un email a [tu-email@example.com] con:
   - Descripción de la vulnerabilidad
   - Pasos para reproducirla
   - Posible impacto
   - Sugerencias de solución (si las tienes)

2. **Tiempo de Respuesta**: Intentaremos responder dentro de 48 horas.

3. **Actualización**: Mantendremos comunicación contigo sobre el progreso de la resolución.

### Proceso

1. **Reporte**: Envías el reporte de seguridad privadamente
2. **Confirmación**: Confirmamos la recepción en 48 horas
3. **Validación**: Validamos y reproducimos el problema
4. **Fix**: Desarrollamos y probamos una solución
5. **Release**: Publicamos un patch de seguridad
6. **Disclosure**: Publicamos los detalles después del patch (coordinado contigo)

## Mejores Prácticas de Seguridad

### Para Usuarios

1. **Credenciales AWS**:
   - Nunca compartas tus credenciales AWS
   - Usa AWS SSO cuando sea posible
   - Rota tus credenciales regularmente
   - Usa roles IAM con permisos mínimos

2. **Kubeconfig**:
   - No compartas tu archivo kubeconfig
   - Usa permisos restrictivos: `chmod 600 ~/.kube/config`
   - No lo versiones en git (ya está en .gitignore)
   - Revisa los backups periódicamente

3. **Ejecución**:
   - Revisa el código antes de ejecutar
   - Usa `--dry-run` primero
   - Verifica los permisos del script: `ls -la auto_kubeconfig.py`

4. **Actualizaciones**:
   - Mantén actualizado Python
   - Mantén actualizado AWS CLI
   - Actualiza el script regularmente

### Para Desarrolladores

1. **Código**:
   - No hardcodear credenciales
   - Validar todas las entradas de usuario
   - Usar subprocess de forma segura
   - Manejar errores apropiadamente

2. **Dependencies**:
   - Revisar dependencias regularmente
   - Usar versiones específicas en requirements.txt
   - Auditar con `pip-audit` o similar

3. **Testing**:
   - Probar con múltiples configuraciones
   - Validar manejo de errores
   - Probar con datos maliciosos

## Consideraciones de Seguridad

### Scope del Script

Este script:
- ✅ Lee configuración de AWS (read-only)
- ✅ Ejecuta comandos AWS CLI
- ✅ Escribe archivo kubeconfig
- ✅ Crea backups automáticos
- ❌ NO expone credenciales
- ❌ NO modifica configuración AWS
- ❌ NO envía datos a servidores externos

### Permisos Requeridos

El script requiere:
- Lectura de `~/.aws/config`
- Ejecución de AWS CLI
- Escritura en `~/.kube/config`
- Permisos AWS: `eks:ListClusters`, `eks:DescribeCluster`

### Almacenamiento de Credenciales

- Las credenciales las maneja AWS CLI
- No se almacenan en el script
- Los tokens los genera `aws eks get-token` dinámicamente
- Los tokens expiran automáticamente según configuración AWS

## Vulnerabilidades Conocidas

Actualmente no hay vulnerabilidades conocidas.

## Actualizaciones de Seguridad

Las actualizaciones de seguridad se publicarán:
- En CHANGELOG.md
- Como releases en GitHub
- Con tag de versión incrementado

## Contacto

Para reportes de seguridad: [tu-email@example.com]

Para otros issues: Usa GitHub Issues

---

**Nota**: Esta política de seguridad puede actualizarse. Revísala periódicamente.

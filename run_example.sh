#!/bin/bash
# Script de ejemplo para ejecutar el generador de kubeconfig

echo "🚀 Auto Kubeconfig Generator - Ejemplos de uso"
echo "================================================"
echo ""
echo "1. Generar kubeconfig con TODOS los profiles:"
echo "   python auto_kubeconfig.py"
echo ""
echo "2. Ver qué se generaría (dry-run):"
echo "   python auto_kubeconfig.py --dry-run"
echo ""
echo "3. Generar solo para profiles específicos:"
echo "   python auto_kubeconfig.py --profiles profile1 profile2"
echo ""
echo "4. Guardar en ubicación diferente:"
echo "   python auto_kubeconfig.py --output ./custom-config"
echo ""
echo "5. Sin crear backup:"
echo "   python auto_kubeconfig.py --no-backup"
echo ""
echo "================================================"
echo ""
echo "¿Deseas ejecutar el generador ahora? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "Ejecutando generador con dry-run para ver qué se encontrará..."
    python auto_kubeconfig.py --dry-run
    echo ""
    echo "¿Deseas generar el archivo real? (y/n)"
    read -r response2
    
    if [[ "$response2" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        python auto_kubeconfig.py
    else
        echo "Operación cancelada"
    fi
else
    echo "Para ejecutar más tarde, usa: python auto_kubeconfig.py"
fi

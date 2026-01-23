#!/usr/bin/env python3
"""
Add Error Handling and Email Notification to Gas Station Analyzer Workflow
This script adds professional error handling with email notifications
"""

import json
import sys
from pathlib import Path

def add_error_handling_nodes(workflow_path: str) -> None:
    """Add error handling and email notification nodes to the workflow"""
    
    # Load existing workflow
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    print(f"✅ Loaded workflow: {workflow['name']}")
    print(f"📊 Current nodes: {len(workflow['nodes'])}")
    
    # Define new nodes for error handling
    error_trigger_node = {
        "parameters": {},
        "id": "error-trigger-node",
        "name": "Error Trigger",
        "type": "n8n-nodes-base.errorTrigger",
        "typeVersion": 1,
        "position": [1200, 600]
    }
    
    format_error_node = {
        "parameters": {
            "jsCode": """// Format error message for email notification
const error = $input.first().json;
const workflowName = "Gas Station Analyzer";

// Extract error details
const errorMessage = error.message || 'Unknown error';
const errorNode = error.node?.name || 'Unknown node';
const errorTime = new Date().toLocaleString('es-MX', { 
  timeZone: 'America/Mexico_City',
  dateStyle: 'full',
  timeStyle: 'long'
});

// Build formatted message
const emailSubject = `🚨 Error en ${workflowName}`;
const emailBody = `
<h2 style="color: #d32f2f;">⚠️ Error Detectado en Workflow</h2>

<div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
  <p><strong>📋 Workflow:</strong> ${workflowName}</p>
  <p><strong>🔴 Nodo con Error:</strong> ${errorNode}</p>
  <p><strong>⏰ Fecha y Hora:</strong> ${errorTime}</p>
</div>

<div style="background-color: #ffebee; padding: 15px; border-radius: 5px; border-left: 4px solid #d32f2f;">
  <h3 style="color: #d32f2f; margin-top: 0;">Mensaje de Error:</h3>
  <pre style="white-space: pre-wrap; word-wrap: break-word;">${errorMessage}</pre>
</div>

<div style="margin-top: 20px; padding: 15px; background-color: #e3f2fd; border-radius: 5px;">
  <h3 style="color: #1976d2; margin-top: 0;">🔧 Acciones Recomendadas:</h3>
  <ul>
    <li>Revisa el nodo <strong>${errorNode}</strong> en n8n</li>
    <li>Verifica las credenciales de APIs (Apify, Google Sheets, Google Places)</li>
    <li>Confirma que los datos de entrada sean válidos</li>
    <li>Revisa los logs completos en n8n: <a href="http://localhost:5678">http://localhost:5678</a></li>
  </ul>
</div>

<hr style="margin: 30px 0; border: none; border-top: 1px solid #ccc;">

<p style="color: #666; font-size: 12px;">
  Este es un mensaje automático del sistema de monitoreo de workflows n8n.<br>
  Para más información, contacta al administrador del sistema.
</p>
`;

return [{
  json: {
    subject: emailSubject,
    body: emailBody,
    errorNode: errorNode,
    errorMessage: errorMessage,
    timestamp: errorTime
  }
}];"""
        },
        "id": "format-error-message",
        "name": "Format Error Message",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1424, 600]
    }
    
    send_email_node = {
        "parameters": {
            "fromEmail": "noreply@gasstationanalyzer.com",
            "toEmail": "admin@example.com",  # Usuario debe cambiar esto
            "subject": "={{ $json.subject }}",
            "emailType": "html",
            "message": "={{ $json.body }}",
            "options": {}
        },
        "id": "send-error-email",
        "name": "Send Error Email",
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": [1648, 600],
        "credentials": {
            "smtp": {
                "id": "SMTP_CREDENTIAL_ID",  # Usuario debe configurar credenciales SMTP
                "name": "SMTP account"
            }
        },
        "notes": "⚠️ CONFIGURAR: Actualiza 'toEmail' con tu email y configura credenciales SMTP en n8n"
    }
    
    # Add sticky note for error handling section
    error_sticky_note = {
        "parameters": {
            "content": """## 🚨 ERROR HANDLING
- Captura errores de cualquier nodo del workflow
- Formatea mensaje con detalles del error
- Envía notificación por email al administrador
- **⚠️ IMPORTANTE:** Configura credenciales SMTP y email de destino""",
            "height": 180,
            "width": 580,
            "color": 7  # Red color for errors
        },
        "id": "error-handling-sticky",
        "name": "Sticky Note - Error Handling",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [1200, 400]
    }
    
    # Add nodes to workflow
    new_nodes = [
        error_trigger_node,
        format_error_node,
        send_email_node,
        error_sticky_note
    ]
    
    workflow['nodes'].extend(new_nodes)
    
    # Add connections
    if 'connections' not in workflow:
        workflow['connections'] = {}
    
    workflow['connections']['Error Trigger'] = {
        "main": [[{"node": "Format Error Message", "type": "main", "index": 0}]]
    }
    
    workflow['connections']['Format Error Message'] = {
        "main": [[{"node": "Send Error Email", "type": "main", "index": 0}]]
    }
    
    # Save updated workflow
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Error handling nodes added successfully!")
    print(f"📊 Total nodes now: {len(workflow['nodes'])}")
    print(f"\n📝 NEXT STEPS:")
    print(f"   1. Abre n8n: http://localhost:5678")
    print(f"   2. Abre el workflow 'Gas Station Analyzer'")
    print(f"   3. Configura credenciales SMTP en el nodo 'Send Error Email'")
    print(f"   4. Actualiza el email de destino en 'toEmail'")
    print(f"   5. Guarda el workflow")
    print(f"\n🎯 Los siguientes nodos fueron agregados:")
    print(f"   - Error Trigger (captura errores)")
    print(f"   - Format Error Message (formatea mensaje)")
    print(f"   - Send Error Email (envía notificación)")
    print(f"   - Sticky Note - Error Handling (documentación)")

if __name__ == "__main__":
    # Get workflow path
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    workflow_path = project_root / "workflows" / "gas_station_analyzer.json"
    
    if not workflow_path.exists():
        print(f"❌ Error: Workflow file not found at {workflow_path}")
        sys.exit(1)
    
    print("🚀 Adding Error Handling to Gas Station Analyzer Workflow\n")
    add_error_handling_nodes(str(workflow_path))
    print("\n✨ Done!")

import json
import os
from typing import Optional, Dict, Any

# Define the paths relative to your project root
TASKS_DIR = "doc/tasks"

def get_next_agent_task(adr_id: str) -> str:
    """
    Finds and returns the single next pending task for a given ADR ID.
    If a phase is complete but awaits human verification, it blocks advancement.
    
    Args:
        adr_id: The ID of the ADR (e.g., 'ADR-004')
        
    Returns:
        A JSON string containing the next task to execute, or a status message.
    """
    file_path = os.path.join(TASKS_DIR, f"{adr_id}_pipeline.json")
    
    if not os.path.exists(file_path):
        return json.dumps({"error": f"Pipeline file not found at {file_path}"})
        
    with open(file_path, "r", encoding="utf-8") as f:
        pipeline_data = json.load(f)
        
    # Iterate through the phases sequentially
    for phase in pipeline_data.get("pipeline", []):
        # If this phase is completely done, skip to the next one
        if phase.get("status") == "completed":
            continue
            
        # Check if all tasks in this phase are done, but the phase gate hasn't cleared
        all_tasks_done = all(t.get("status") == "completed" for t in phase.get("tasks", []))
        if all_tasks_done and phase.get("status") != "completed":
            return json.dumps({
                "status": "TRIGGER_QUALITY_GATE",
                "message": f"Phase {phase.get('phase_number', 'unknown')} tasks are finished. You must now invoke the 'quality-checker' skill to verify the phase gate.",
                "phase_gate": phase.get("phase_gate"),
                "next_action": "Call the 'quality-checker' skill before the pipeline can advance."
            }, indent=2)
            
        # Find the first task in this phase that isn't completed yet
        for task in phase.get("tasks", []):
            if task.get("status") in ["pending", "failed", "in_progress"]:
                
                # Check dependencies before returning it to the agent
                dependencies = task.get("scope", {}).get("dependencies", [])
                # If you want to check if dependencies from past phases failed, you can do it here
                
                # Build a lightweight task payload for the agent to save context tokens
                agent_payload = {
                    "status": "READY_TO_EXECUTE",
                    "adr_id": pipeline_data.get("adr_id"),
                    "global_context": pipeline_data.get("global_context"),
                    "phase_name": phase.get("phase_name"),
                    "task_id": task.get("task_id"),
                    "title": task.get("title"),
                    "target_files": task.get("scope", {}).get("target_files", []),
                    "instructions": task.get("instructions"),
                    "acceptance_criteria": task.get("acceptance_criteria"),
                    "output_format": task.get("output_format")
                }
                return json.dumps(agent_payload, indent=2)
                
    return json.dumps({"status": "FINISHED", "message": "All phases and tasks for this ADR are completed!"})

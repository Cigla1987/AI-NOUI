document.addEventListener('DOMContentLoaded', () => {
  // Popup for creating project
  function showProjectPopup() {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.background = 'rgba(0,0,0,0.3)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = 1000;

    // Create popup
    const popup = document.createElement('div');
    popup.style.background = '#fff';
    popup.style.padding = '2rem';
    popup.style.borderRadius = '8px';
    popup.style.boxShadow = '0 2px 12px rgba(44,62,80,0.15)';
    popup.style.minWidth = '320px';

    popup.innerHTML = `
      <h2>Create Project</h2>
      <label>Project Name:</label><br>
      <input type="text" id="project-name" style="width:100%;margin-bottom:1rem;"><br>
      <label>Short Description:</label><br>
      <textarea id="project-desc" style="width:100%;height:60px;margin-bottom:1rem;"></textarea><br>
      <button id="popup-create">Create</button>
      <button id="popup-cancel" style="margin-left:1rem;">Cancel</button>
    `;

    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    document.getElementById('popup-cancel').onclick = () => {
      document.body.removeChild(overlay);
    };
    document.getElementById('popup-create').onclick = async () => {
      const name = document.getElementById('project-name').value.trim();
      const desc = document.getElementById('project-desc').value.trim();
      if (!name) {
        alert('Project name required!');
        return;
      }
      // Send project info to backend
      try {
        const res = await fetch('/api/project', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, description: desc })
        });
        if (res.ok) {
          alert('Project created and saved!');
        } else {
          alert('Failed to save project.');
        }
      } catch (e) {
        alert('Error saving project: ' + e);
      }
      document.body.removeChild(overlay);
    };
  }

  // Attach to Create Project button
  const createProjectBtn = document.getElementById('create-project');
  if (createProjectBtn) {
    createProjectBtn.addEventListener('click', showProjectPopup);
  }

  // Project Buildup button logic
  const buildupBtn = document.getElementById('project-buildup');
  const canvasElem = document.getElementById('canvas');
  const rightSidemenu = document.getElementById('right-sidemenu');
  if (canvasElem) canvasElem.style.display = 'none';
  if (rightSidemenu) rightSidemenu.style.display = 'none';
  if (buildupBtn) {
    buildupBtn.addEventListener('click', async () => {
      // Call backend to set buildup state
      try {
        const res = await fetch('/api/buildup', { method: 'POST' });
        if (res.ok) {
          window.location.href = '/dashboard';
        } else {
          alert('Project buildup failed.');
        }
      } catch (e) {
        alert('Error during buildup: ' + e);
      }
    });
  }
  const components = document.querySelectorAll('#components-list .component');
  const layout = []; // keeps track of components on canvas

  // Make components draggable
  components.forEach(c => {
    c.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', c.dataset.kind);
    });
  });

  // Allow drop
  canvas.addEventListener('dragover', e => e.preventDefault());

  canvas.addEventListener('drop', e => {
    e.preventDefault();
    const kind = e.dataTransfer.getData('text/plain');
    if (!kind) return;

    // Ask user for pin number
    let pin = prompt(`Assign pin number for ${kind}:`, "2");
    if (!pin) return;

    // Get mouse position relative to canvas
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Create a visual element on canvas
    const compEl = document.createElement('div');
    compEl.className = 'canvas-component';
    compEl.textContent = `${kind} (Pin ${pin})`;
    compEl.style.position = 'absolute';
    compEl.style.left = x + 'px';
    compEl.style.top = y + 'px';
    compEl.style.padding = '5px 10px';
    compEl.style.margin = '5px';
    compEl.style.border = '1px solid #34495e';
    compEl.style.background = '#ecf0f1';
    canvas.appendChild(compEl);

    // Add to layout array
    layout.push({
      kind: kind,
      pin: pin,
      x: x,
      y: y,
      thresh: null,
      sec: null
    });

    console.log('Current layout:', layout);
  });

  // Generate code button
  const generateBtn = document.getElementById('generate');
  generateBtn.addEventListener('click', async () => {
    const promptText = document.getElementById('prompt').value;
    if (!promptText) {
      alert('Enter a prompt first!');
      return;
    }

    const response = await fetch('/ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: promptText, layout })
    });

    const data = await response.json();
    if (data.success) {
      document.getElementById('code').value = data.code;
    } else {
      alert('AI failed: ' + (data.error || 'unknown error'));
    }
  });

  // Download button
  const downloadBtn = document.getElementById('download');
  downloadBtn.addEventListener('click', () => {
    const promptText = document.getElementById('prompt').value;
    const url = `/download?prompt=${encodeURIComponent(promptText)}`;
    window.location.href = url;
  });
});

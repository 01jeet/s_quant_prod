HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Infrastructure Health</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #1a1a1a; color: white; text-align: center; 
            margin: 0; padding: 0;
        }
        .container { 
            max-width: 800px; margin: 50px auto; padding: 20px; 
            background: #2d2d2d; border-radius: 15px; 
            box-shadow: 0 0 20px rgba(0,0,0,0.5); 
        }
        h1 { color: #eee; margin-bottom: 30px; }
        .service-row { 
            display: flex; justify-content: space-between; align-items: center; 
            padding: 15px 20px; border-bottom: 1px solid #444; 
        }
        .service-name { font-size: 1.2rem; font-weight: bold; }
        .status-light {
            width: 15px; height: 15px; border-radius: 50%; 
            display: inline-block; margin-right: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        .healthy { background-color: #2ecc71; box-shadow: 0 0 15px #2ecc71; }
        .unhealthy { background-color: #e74c3c; box-shadow: 0 0 15px #e74c3c; }
        .starting { background-color: #f1c40f; box-shadow: 0 0 15px #f1c40f; }
        .unknown { background-color: #95a5a6; }
        .last-update { margin-top: 20px; font-size: 0.8rem; color: #888; }
    </style>
    <script>
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                const list = document.getElementById('service-list');
                list.innerHTML = '';
                
                data.forEach(service => {
                    const row = document.createElement('div');
                    row.className = 'service-row';
                    
                    let lightClass = 'unknown';
                    if(service.status === 'healthy') lightClass = 'healthy';
                    else if(service.status === 'unhealthy') lightClass = 'unhealthy';
                    else if(service.status === 'starting') lightClass = 'starting';

                    row.innerHTML = `
                        <span class="service-name">${service.name}</span>
                        <div>
                            <span class="status-light ${lightClass}"></span>
                            <span>${service.status.toUpperCase()}</span>
                        </div>
                    `;
                    list.appendChild(row);
                });
                document.getElementById('time').innerText = "Last Updated: " + new Date().toLocaleTimeString();
            } catch (error) {
                console.error("Error fetching status:", error);
            }
        }
        // Check every 5 seconds
        setInterval(updateStatus, 5000);
        // Initial load
        window.onload = updateStatus;
    </script>
</head>
<body>
    <div class="container">
        <h1>🚀 Infra Health Monitor</h1>
        <div id="service-list">Loading services...</div>
        <div class="last-update" id="time"></div>
    </div>
</body>
</html>
"""
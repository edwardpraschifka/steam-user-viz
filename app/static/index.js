import * as THREE from 'https://esm.sh/three';

const sessionId = crypto.randomUUID();

const Graph = new ForceGraph3D(document.getElementById('3d-graph'))
            .nodeThreeObject(({ avatarurl }) => {
                const imgTexture = new THREE.TextureLoader().load(avatarurl);
                imgTexture.colorSpace = THREE.SRGBColorSpace;
                const material = new THREE.SpriteMaterial({ map: imgTexture });
                const sprite = new THREE.Sprite(material);
                sprite.scale.set(12, 12);
                return sprite;
            })
            .onNodeClick(node => {
                console.log(node.id)
                handleExpand(node.id)
            })


async function renderGraph(gData) {
    Graph.graphData(gData["data"])
}

async function handleSubmit() {
    const id = document.getElementById("id").value;

    const response = await fetch("/graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, session_id: sessionId, skip_self: 0 })
    });

    const gData = await response.json();

    if (response.ok && gData["success"]) {
        renderGraph(gData)
    }
}

async function handleExpand(id) {
    const response = await fetch("/graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, session_id: sessionId, skip_self: 0 })
    });

    const gData = await response.json();

    console.log(gData)
    
    
    if (response.ok && gData["success"]) {
        renderGraph(gData)
    }
}

document.getElementById("submit-btn").addEventListener("click", handleSubmit);
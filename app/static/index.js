import * as THREE from 'https://esm.sh/three';

const sessionId = crypto.randomUUID();

const Graph = new ForceGraph3D(document.getElementById('graph'))
            .nodeThreeObject(({ avatarurl }) => {
                const imgTexture = new THREE.TextureLoader().load(avatarurl);
                imgTexture.colorSpace = THREE.SRGBColorSpace;
                const material = new THREE.SpriteMaterial({ map: imgTexture });
                const sprite = new THREE.Sprite(material);
                sprite.scale.set(12, 12);
                return sprite;
            })
            .onNodeClick(node => {
                handleExpand(node.id);
            })
            .onNodeRightClick(node => {
                openSidebar(node.id);
            })


async function renderGraph(gData) {
    Graph.graphData(gData)
}

async function handleSubmit() {
    const id = document.getElementById("id").value;
    handleExpand(id)
}

async function handleExpand(id) {
    const response = await fetch("/graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, session_id: sessionId, skip_self: 0 })
    });

    const gData = await response.json();

    console.log(gData)
    
    
    if (response.ok && gData["private"] == "False") {
        renderGraph(gData["data"])
    }
}

async function getProfile(id) {
    const response = await fetch(`/games?id=${id}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    });

    const games = await response.json();
    return games
}

async function openSidebar(id) {
    const profile = await getProfile(id);
    console.log(profile)

    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle('open');
}

document.getElementById("submit-btn").addEventListener("click", handleSubmit);
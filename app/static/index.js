import * as THREE from 'https://esm.sh/three';
import { id_list } from './random_ids.js';

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
                openSidebar(node);
            })


const seenNodeIds = new Set();

async function renderGraph(gData) {
    let unSeenIds = 0;

    for (const node of gData.nodes) {
        if (!seenNodeIds.has(node.id)) {
            seenNodeIds.add(node.id);
            unSeenIds++;
        }
    }

    Graph.graphData(gData)
    showToast(`Added ${unSeenIds} users to graph`)
    updateNodeCounter()
}

function updateNodeCounter() {
    document.getElementById("node-counter").textContent = `${seenNodeIds.size} users in graph`;
}

function isValidSteamId(id) {
    return /^7656119\d{10}$/.test(id);
}

const TOAST_STYLE = {
    background: "rgba(20, 22, 34, 0.9)",
    color: "rgba(255, 255, 255, 0.85)",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    fontSize: "13.5px",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    borderRadius: "12px",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)",
    backdropFilter: "blur(16px)",
    WebkitBackdropFilter: "blur(16px)",
};

function showToast(message) {
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        style: TOAST_STYLE,
    }).showToast();
}

async function handleSubmit() {
    const id = document.getElementById("id").value.trim();

    if (!isValidSteamId(id)) {
        showToast("Please enter a valid SteamID (e.g. 76561198202745727)");
        return;
    }

    handleExpand(id)
}

async function handleRandom() {
    const idx = Math.floor(Math.random() * id_list.length)
    const id = id_list[idx]
    handleExpand(id)
}

function loaderStart() {
    document.getElementById("loader").classList.add("loading");
}

function loaderStop() {
    document.getElementById("loader").classList.remove("loading");
}

async function handleExpand(id) {
    openInstructions()
    loaderStart();
    try {
        const response = await fetch("/graph", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id, session_id: sessionId, skip_self: 0 })
        });

        const gData = await response.json();

        if (response.ok && gData["private"] == "False") {
            renderGraph(gData["data"])
        } else if (response.ok && gData["private"] == "True") {
            showToast("This user's account is private.")
        }
        
    } finally {
        loaderStop();
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

async function openSidebar(node) {
    const profile = await getProfile(node.id);

    const sidebar = document.getElementById("sidebar");

    const games = profile.all?.games ?? [];
    const recentGames = profile.recently_played?.games ?? [];
    const sortedGames = [...games].sort((a, b) => b.playtime_forever - a.playtime_forever);

    const formatHours = (mins) => {
        const h = Math.round(mins / 60);
        return h === 1 ? '1 hr' : `${h} hrs`;
    };

    const iconUrl = (appid, hash) =>
        `https://media.steampowered.com/steamcommunity/public/images/apps/${appid}/${hash}.jpg`;

    const storeUrl = (appid) => `https://store.steampowered.com/app/${appid}`;

    const gameRow = (game) => `
        <a class="sidebar-game" href="${storeUrl(game.appid)}" target="_blank" rel="noopener noreferrer">
            <img class="sidebar-game-icon" src="${iconUrl(game.appid, game.img_icon_url)}" alt="">
            <span class="sidebar-game-name">${game.name}</span>
            <span class="sidebar-game-hours">${formatHours(game.playtime_forever)}</span>
        </a>`;

    sidebar.innerHTML = `
        <div class="sidebar-header">
            <button class="sidebar-close" onclick="closeSidebar()">✕</button>
        </div>
        <div class="sidebar-user">
            <img class="sidebar-avatar" src="${node.avatarurl}" alt="">
            <div class="sidebar-user-info">
                <a class="sidebar-username" href="${node.profileurl}" target="_blank">${node.name}</a>
                <span class="sidebar-game-count">${games.length} games owned</span>
            </div>
        </div>
        ${recentGames.length > 0 ? `
            <div class="sidebar-section-label">Recently Played</div>
            ${recentGames.map(gameRow).join('')}
        ` : ''}
        <div class="sidebar-section-label">All Games</div>
        ${sortedGames.map(gameRow).join('')}
    `;

    sidebar.classList.add('open');
}

window.closeSidebar = function() {
    document.getElementById("sidebar").classList.remove('open');
}

function openInstructions() {
    document.getElementById("instructions").classList.remove('hidden');
}

document.getElementById("submit-btn").addEventListener("click", handleSubmit);
document.getElementById("random-btn").addEventListener("click", handleRandom);
Graph.onEngineStop(() => Graph.zoomToFit(400));
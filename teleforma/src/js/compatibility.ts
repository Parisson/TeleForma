window.addEventListener("DOMContentLoaded", () => {

    const testVideo = document.createElement("video");
    if (testVideo.canPlayType) {
        // Check for Webm support
        const webm = "" !== testVideo.canPlayType('video/webm; codecs="vp8, vorbis"');
        if (webm){
            const container = document.getElementById("content");
            if(container){
                const p = document.createElement("p");
                p.classList.add("warning");
                container.prepend(p);
                p.innerHTML = `
                    Votre navigateur n'est pas compatible avec le format video <abbr title="WebM est un format de fichier multimédia ouvert, principalement destiné à un usage sur le web.">WebM</abbr> des cours en direct.
                    Veuillez téléchargez Firefox ou Google Chrome dans leur dernière version.
                `;
            }
        }
        
    }
});
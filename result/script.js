document.addEventListener("DOMContentLoaded", () => {
    const commitList = document.getElementById("commit-list");

    for (const author in jsonData) {
        const authorCommits = jsonData[author];
        authorCommits.forEach(commit => {
            const commitElement = document.createElement("div");
            commitElement.classList.add("commit");

            const commitTitle = document.createElement("h2");
            commitTitle.innerText = `${author} - Commit #${commit.commit_number}: ${commit.commit_message}`;
            commitTitle.addEventListener("click", () => {
                commitDetails.classList.toggle("commit-details");
                commitDetails.style.display = commitDetails.style.display === "none" ? "block" : "none";
            });

            const commitDetails = document.createElement("div");
            commitDetails.classList.add("commit-details");
            commitDetails.innerHTML = `
                <p><strong>Time Diff:</strong> ${commit.time_diff}</p>
                <p><strong>Diff Mass:</strong> ${commit.diff_mass}</p>
                <p><strong>Density:</strong> ${commit.density}</p>
                <p><strong>Commit Message Analysis:</strong></p>
                <pre>${commit.commit_message_analysis}</pre>
                <p><strong>Diff Text:</strong></p>
                <pre>${commit.diff_text}</pre>
            `;

            commitElement.appendChild(commitTitle);
            commitElement.appendChild(commitDetails);
            commitList.appendChild(commitElement);
        });
    }
});

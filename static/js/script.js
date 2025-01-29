let currentSessionId = null; // Initialize currentSessionId globally

window.onload = function () {
      currentSessionId = null; // Reset session ID on page load

      // Hide the output-container and show the file-upload-container on load
      document.getElementById("output-container").style.display = "none";
      document.getElementById("file-upload-container").style.display = "grid";
      document.getElementById("writeTranscriptOutput").style.display = "none";

      // Clear chat container on page load
      // document.getElementById("output-container").innerHTML = "";
};

function generateSessionId() {
      return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
            const r = (Math.random() * 16) | 0;
            const v = c === "x" ? r : (r & 0x3) | 0x8;
            return v.toString(16);
      });
}

document.querySelector(".new-session-button").addEventListener("click", function () {
      location.reload(); // Refresh the page
});

const toggleThemeButton = document.getElementById("theme-toggle");

// Load the preferred theme from localStorage
const currentTheme = localStorage.getItem("theme") || "light-mode";
document.documentElement.classList.add(currentTheme); // Apply theme to the html tag
toggleThemeButton.textContent = currentTheme === "dark-mode" ? "Switch to Light Mode" : "Switch to Dark Mode";

// Toggle theme on button click
toggleThemeButton.addEventListener("click", () => {
      const html = document.documentElement; // Target the html element
      if (html.classList.contains("dark-mode")) {
            html.classList.replace("dark-mode", "light-mode");
            toggleThemeButton.textContent = "Switch to Dark Mode";
            localStorage.setItem("theme", "light-mode");
            html.style.backgroundColor = "#ffffff"; // Apply background color to html
      } else {
            html.classList.replace("light-mode", "dark-mode");
            toggleThemeButton.textContent = "Switch to Light Mode";
            localStorage.setItem("theme", "dark-mode");
            html.style.backgroundColor = "#252525"; // Apply background color to html
      }
});

// Event listener for selecting a session from the sidebar
document.querySelectorAll(".sidebar-session-item").forEach((sessionItem) => {
      sessionItem.addEventListener("click", function () {
            // Add logic here to load the session data
            const sessionId = this.dataset.sessionId; // Assuming session ID is stored in a data attribute
            loadSessionData(sessionId);
      });
});

/////////////////////////////////////////////////////////
//                  Utility functions                  //
/////////////////////////////////////////////////////////

function scrollToBottom() {
      const chatContainer = document.getElementById("session-container");
      chatContainer.scrollTop = chatContainer.scrollHeight;
}
function handlePaste(event) {
      event.preventDefault();
      const text = event.clipboardData.getData("text/plain");
      document.execCommand("insertText", false, text);
}

function loadingAnimation() {
      const chatContainer = document.getElementById("session-container");
      const loadingMessageContainer = document.createElement("div");
      loadingMessageContainer.classList.add("bot-loading-message-container");
      loadingMessageContainer.id = "slide-loading-animation";
      chatContainer.appendChild(loadingMessageContainer);
}

function resetSendButton() {
      const userInput = document.getElementById("userInput");
      const sendButton = document.getElementById("sendButton");
      const sendIcon = document.getElementById("sendIcon");

      userInput.setAttribute("contenteditable", "true");
      sendButton.disabled = false;
      sendIcon.src = "static/images/arrow-left.svg";
      sendIcon.onclick = null; // Remove the stopStream function from the click event
}

function cleanInput() {
      const userInput = document.getElementById("userInput");
      userInput.innerHTML = userInput.innerHTML.replace(/<span[^>]*>(.*?)<\/span>/g, "$1");
}

/////////////////////////////////////////////////////////
//                  sidebar functions                  //
/////////////////////////////////////////////////////////

async function clearAllChats() {
      // Show confirmation dialog
      const confirmation = confirm("Are you sure you want to clear all chats?");
      if (!confirmation) {
            return; // Exit if the user cancels
      }

      try {
            // Send POST request to Flask backend to delete all sessions
            const response = await fetch("/delete_all_sessions", {
                  method: "POST",
                  headers: {
                        "Content-Type": "application/json",
                  },
            });

            if (response.ok) {
                  alert("All sessions have been cleared.");
                  location.reload(); // Reload the page to reflect the changes
            } else {
                  const errorMessage = await response.text();
                  alert("Failed to clear sessions: " + errorMessage);
            }
      } catch (error) {
            console.error("Error clearing sessions:", error);
            alert("An error occurred while clearing sessions. Please try again.");
      }
}

async function deleteSession(sessionId) {
      // Show confirmation dialog
      const confirmation = confirm("Are you sure you want to delete this session?");
      if (!confirmation) {
            return; // Exit if the user cancels
      }

      try {
            // Send POST request to Flask backend to delete the specific session
            const response = await fetch("/delete_session", {
                  method: "POST",
                  headers: {
                        "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ session_id: sessionId }),
            });

            if (response.ok) {
                  alert("Session deleted successfully.");
                  // Remove the session from the DOM
                  const sessionElement = document.querySelector(`[session_id="${sessionId}"]`);
                  if (sessionElement) {
                        sessionElement.remove();
                  }
            } else {
                  const errorMessage = await response.text();
                  alert("Failed to delete session: " + errorMessage);
            }
      } catch (error) {
            console.error("Error deleting session:", error);
            alert("An error occurred while deleting the session. Please try again.");
      }
}

async function loadSessionData(sessionId) {
      // Hide the file-upload-container and show the output-container
      document.getElementById("file-upload-container").style.display = "none";
      document.getElementById("output-container").style.display = "grid";
      document.getElementById("writeTranscriptOutput").style.display = "block";

      currentSessionId = sessionId;

      try {
            const response = await fetch("/get_session_data", {
                  method: "POST",
                  headers: {
                        "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ sessionId }),
            });

            if (!response.ok) {
                  throw new Error(`Failed to fetch session data: ${response.status}`);
            }

            const responseData = await response.json(); // Ensure JSON response
            const sessionData = responseData.session_data; // Access 'session_data'

            if (sessionData && sessionData.length > 0) {
                  renderSession(sessionData, sessionId);
            } else {
                  console.log("No session data found for this session.");
            }
      } catch (error) {
            console.error("Error loading session data:", error);
      }
}
const dropZone = document.getElementById("dropZone");
const fileUpload = document.getElementById("fileUpload");

// Add drag-and-drop events
dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("drag-over");

      // Handle dropped files
      const files = e.dataTransfer.files;
      if (files.length) {
            handleFileUpload(files[0]);
      }
});

// Handle click to open file dialog
dropZone.addEventListener("click", () => {
      fileUpload.click();
});

// Handle file selection from file dialog
fileUpload.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
            handleFileUpload(file);
      }
});

async function handleFileUpload(file) {
      if (file) {
            console.log("File uploaded:", file.name);

            // Create a FormData object
            const formData = new FormData();
            formData.append("file", file);

            try {
                  // Auto-submit file
                  const response = await fetch("/read_transcript", {
                        method: "POST",
                        body: formData,
                  });

                  if (!response.ok) {
                        alert("Failed to read transcript.");
                        return;
                  }

                  const data = await response.json();
                  const transcript = data.transcript;

                  processTranscript(transcript);
            } catch (error) {
                  console.error("Error uploading file:", error);
                  alert("Error uploading file.");
            }
      }
}

async function uploadTranscript() {
      const fileInput = document.getElementById("fileUpload");
      const transcriptTextarea = document.getElementById("transcriptInput");
      let transcript = "";

      if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            try {
                  const response = await fetch("/read_transcript", {
                        method: "POST",
                        body: formData,
                  });

                  if (!response.ok) {
                        alert("Failed to read transcript.");
                        return;
                  }

                  const data = await response.json();
                  transcript = data.transcript;
            } catch (error) {
                  console.error("Error uploading file:", error);
                  alert("Error uploading file.");
                  return;
            }
      } else if (transcriptTextarea.value.trim()) {
            transcript = transcriptTextarea.value.trim();
      } else {
            alert("Please upload a file or paste a transcript.");
            return;
      }

      processTranscript(transcript);
}

async function updateSession(participants, summary, notes, actionItems, transcript, sessionIcon, sessionName) {
      try {
            const response = await fetch("/update_session", {
                  method: "POST",
                  headers: {
                        "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                        session_id: currentSessionId,
                        session_icon: sessionIcon,
                        transcript: transcript,
                        participants: participants,
                        summary: summary,
                        notes: notes,
                        action_items: actionItems,
                        session_name: sessionName,
                  }),
            });

            const data = await response.json();
            if (data.success) {
                  console.log("Session updated successfully.");
            } else {
                  console.error("Failed to update session.");
            }
      } catch (error) {
            console.error("Error updating session:", error);
      }
}

function updateSidebarWithSession(sessionId, firstQuestion, session_icon) {
      const sessionList = document.getElementById("session-list");

      // Create the list item for the session
      const sessionItem = document.createElement("li");
      sessionItem.className = "chat-item"; // Set the class name
      sessionItem.setAttribute("session_id", sessionId); // Set the session_id attribute
      sessionItem.onclick = () => loadSessionData(sessionId); // Click handler for the session item

      // Create a div for the emoji container
      const emojiDiv = document.createElement("div");
      emojiDiv.className = "chat-item-emoji"; // Set a class for styling

      // Create the emoji image
      const emojiImage = document.createElement("img");
      emojiImage.className = "emoji-button"; // Add a class for styling
      emojiImage.src = `/static/images/session-icons/${session_icon}`; // Use backticks for template literals

      // Append the emoji image to the emoji container
      emojiDiv.appendChild(emojiImage);

      // Create a div for the session text
      const sessionTextDiv = document.createElement("div");
      sessionTextDiv.className = "chat-item-question"; // Set a class for styling
      sessionTextDiv.textContent = firstQuestion; // Display the first question or a default name

      // Create a div for the delete icon container
      const deleteIconDiv = document.createElement("div");
      deleteIconDiv.className = "chat-item-delete-container"; // Set a class for styling

      // Create the delete icon
      const deleteIcon = document.createElement("img");
      deleteIcon.className = "delete-button"; // Add a class for styling
      deleteIcon.src = "/static/images/delete_black.svg"; // Set the source of the delete icon
      deleteIcon.alt = "Delete"; // Set an alt text for accessibility
      deleteIcon.onclick = (e) => {
            e.stopPropagation(); // Prevent triggering the `onclick` for the session item
            deleteSession(sessionId); // Call the delete function
      };

      // Append the delete icon to the delete icon container
      deleteIconDiv.appendChild(deleteIcon);

      // Create a div for the session indicator
      const indicatorDiv = document.createElement("div");
      indicatorDiv.className = "chat-item-indicator"; // Set a class for styling

      // Append all child elements to the session item
      sessionItem.appendChild(emojiDiv); // Add the emoji container
      sessionItem.appendChild(sessionTextDiv); // Add the session text container
      sessionItem.appendChild(deleteIconDiv); // Add the delete icon container
      sessionItem.appendChild(indicatorDiv); // Add the session indicator

      // Insert the new session item at the top of the list
      sessionList.insertBefore(sessionItem, sessionList.firstChild);
}
function renderSession(sessionData, sessionId) {
      const container = document.getElementById("session-container");
      const participantsOutput = document.getElementById("identifyParticipantsOutput").querySelector(".output-content");
      const summaryOutput = document.getElementById("writeSummaryOutput").querySelector(".output-content");
      const notesOutput = document.getElementById("writeNotesOutput").querySelector(".output-content");
      const actionItemsOutput = document.getElementById("writeActionItemsOutput").querySelector(".output-content");
      const transcriptOutput = document.getElementById("writeTranscriptOutput").querySelector(".output-content");

      // Clear any existing content in the sections
      participantsOutput.innerHTML = "";
      summaryOutput.innerHTML = "";
      notesOutput.innerHTML = "";
      actionItemsOutput.innerHTML = "";
      transcriptOutput.innerHTML = "";

      // Iterate through the session data
      sessionData.forEach((item) => {
            try {
                  // Destructure session data for better readability
                  const { session_icon, transcript, participants, summary, notes, action_items, session_name } = item;

                  // Parse participants from string to a list
                  if (participants && typeof participants === "string") {
                        const participantList = participants
                              .split("\n") // Split the string into lines
                              .filter((line) => line.trim().startsWith("-")) // Keep lines starting with "-"
                              .map((line) => line.replace(/^-\s*/, "")) // Remove "- " prefix
                              .map(
                                    (name) => `
                        <li class="participant-item">
                            <div class="participant-icon">
                                <img src="/static/images/participant-icon.svg" alt="${name}" />
                            </div>
                            <span class="participant-name">${name}</span>
                        </li>
                    `
                              )
                              .join("");

                        participantsOutput.innerHTML = `
                    <ul class="participant-list">
                        ${participantList}
                    </ul>
                `;
                  } else {
                        participantsOutput.textContent = "No participants available.";
                  }

                  // Update other sections
                  summaryOutput.innerHTML = marked.parse(summary) || "N/A";
                  notesOutput.innerHTML = marked.parse(notes) || "N/A";
                  actionItemsOutput.innerHTML = marked.parse(action_items) || "N/A";
                  transcriptOutput.innerHTML = marked.parse(transcript) || "N/A";

                  // Update the session icon dynamically
                  const sessionIconContainer = document.getElementById("session-icon-container");
                  if (sessionIconContainer) {
                        const iconElement = document.createElement("img");
                        iconElement.src = session_icon ? `/static/images/session-icons/${session_icon}` : "/static/images/default-icon.png";
                        iconElement.alt = "Session Icon";
                        iconElement.className = "session-icon";
                        sessionIconContainer.innerHTML = ""; // Clear any previous icon
                        sessionIconContainer.appendChild(iconElement);
                  }
            } catch (error) {
                  console.error("Error rendering session data:", error);
            }
      });
}

async function processTranscript(transcript) {
    // Hide the file-upload-container and show the output-container
    document.getElementById("file-upload-container").style.display = "none";
    document.getElementById("output-container").style.display = "grid";
    document.getElementById("writeTranscriptOutput").style.display = "block";

    const components = ["identify_participants", "write_summary", "write_notes", "write_action_items"];


    document.getElementById("identifyParticipantsOutput").style.display = "none";
    document.getElementById("writeSummaryOutput").style.display = "none";
    document.getElementById("writeNotesOutput").style.display = "none";
    document.getElementById("writeActionItemsOutput").style.display = "none";


    const outputContainers = {
          identify_participants: document.getElementById("identifyParticipantsOutput").querySelector(".output-content"),
          write_summary: document.getElementById("writeSummaryOutput").querySelector(".output-content"),
          write_notes: document.getElementById("writeNotesOutput").querySelector(".output-content"),
          write_action_items: document.getElementById("writeActionItemsOutput").querySelector(".output-content"),
    };

    const transcriptOutput = document.getElementById("writeTranscriptOutput").querySelector(".output-content");
    transcriptOutput.innerHTML = "";
    transcriptOutput.innerHTML = transcript || "N/A";

    let participants, summary, notes, actionItems;

    for (const component of components) {
          const outputContainer = outputContainers[component];
          outputContainer.innerHTML = ""; // Clear previous output

          try {
                const response = await fetch("/invoke_agent", {
                      method: "POST",
                      headers: {
                            "Content-Type": "application/json",
                      },
                      body: JSON.stringify({
                            transcript: transcript,
                            component: component,
                      }),
                });

                if (!response.ok) {
                      outputContainer.innerText = "Error: Failed to fetch response.";
                      continue;
                }
                // Store the results based on the component
                if (component === "identify_participants") {
                    document.getElementById("identifyParticipantsOutput").style.display = "block";
                } else if (component === "write_summary") {
                    document.getElementById("writeSummaryOutput").style.display = "block";
                } else if (component === "write_notes") {
                    document.getElementById("writeNotesOutput").style.display = "block";
                } else if (component === "write_action_items") {
                    document.getElementById("writeActionItemsOutput").style.display = "block";
            }

                // Stream the response
                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let done = false;
                let outputText = "";

                while (!done) {
                      const { value, done: readerDone } = await reader.read();
                      done = readerDone;
                      window.scrollTo({
                        top: document.body.scrollHeight,
                        behavior: "smooth"
                      });

                      if (value) {
                            outputText += decoder.decode(value);

                            if (component === "identify_participants") {
                                  const participantList = outputText
                                        .split("\n")
                                        .filter((line) => line.trim().startsWith("-"))
                                        .map((line) => line.replace(/^-\s*/, ""))
                                        .map(
                                              (name) => `
                              <li class="participant-item">
                                  <div class="participant-icon">
                                      <img src="/static/images/participant-icon.svg" alt="${name}" />
                                  </div>
                                  <span class="participant-name">${name}</span>
                              </li>
                          `
                                        )
                                        .join("");

                                  outputContainer.innerHTML = `
                          <ul class="participant-list">
                              ${participantList}
                          </ul>
                      `;
                            } else {
                                  outputContainer.innerHTML = marked.parse(outputText);
                            }
                      }

                      // Scroll to the latest content in case of overflow
                      outputContainer.scrollTop = outputContainer.scrollHeight;
                }

                // Store the results based on the component
                if (component === "identify_participants") {
                        participants = outputText;
                        document.getElementById("identifyParticipantsOutput").style.display = "block";
                    } else if (component === "write_summary") {
                        summary = outputText;
                        document.getElementById("writeSummaryOutput").style.display = "block";
                    } else if (component === "write_notes") {
                        notes = outputText;
                        document.getElementById("writeNotesOutput").style.display = "block";
                    } else if (component === "write_action_items") {
                        actionItems = outputText;
                        document.getElementById("writeActionItemsOutput").style.display = "block";
                }
          } catch (error) {
                console.error(`Error processing component '${component}':`, error);
                outputContainer.innerText = "Error: Unable to process component.";
          }
    }

    // Generate a session ID if not already set
    if (!currentSessionId) {
          currentSessionId = generateSessionId();
    }

    // Fetch the session icon
    let sessionIcon = null;
    try {
          const iconResponse = await fetch("/get_random_session_icon", {
                method: "POST",
                headers: {
                      "Content-Type": "application/json",
                },
                body: JSON.stringify({ session_id: currentSessionId }),
          });

          if (!iconResponse.ok) {
                console.error("Error fetching session icon:", iconResponse.statusText);
                throw new Error("Failed to fetch session icon");
          }

          const iconData = await iconResponse.json();
          sessionIcon = iconData.relavant_schema;
    } catch (error) {
          console.error("Error fetching session icon:", error);
    }

    // Fetch the session name
    let sessionName = "Untitled Session";
    try {
          const nameResponse = await fetch("/get_session_name", {
                method: "POST",
                headers: {
                      "Content-Type": "application/json",
                },
                body: JSON.stringify({ transcript: transcript }),
          });

          if (!nameResponse.ok) {
                console.error("Error fetching session name:", nameResponse.statusText);
                throw new Error("Failed to fetch session name");
          }

          const nameData = await nameResponse.json();
          sessionName = nameData.session_name || "Untitled Session";
    } catch (error) {
          console.error("Error fetching session name:", error);
    }

    // Update the sidebar with the new session
    updateSidebarWithSession(currentSessionId, sessionName, sessionIcon);

    // Update the session with session name
    await updateSession(participants, summary, notes, actionItems, transcript, sessionIcon, sessionName);
}

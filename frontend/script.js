// =====================================================
// OMNIAI - FRONTEND JAVASCRIPT
// =====================================================


// =====================================================
// QUICK EXAMPLES
// =====================================================

function setExample(type) {

    const input = document.getElementById("userRequest");

    if (!input) return;

    const examples = {

        fashion:
            "I want a stylish birthday dress under ₹2000 from Myntra",

        electronics:
            "I want a Samsung smartphone under ₹30000",

        food:
            "I want spicy biryani under ₹300",

        mens:
            "I want black men's heeled boots for a party under ₹3000"

    };

    input.value = examples[type] || "";

    input.focus();

}


// =====================================================
// FOCUS SEARCH
// =====================================================

function focusSearch() {

    const input = document.getElementById("userRequest");

    if (!input) return;

    input.focus();

    input.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// =====================================================
// GET RECOMMENDATIONS
// =====================================================

async function getRecommendations() {

    const input = document.getElementById("userRequest");
    const results = document.getElementById("results");
    const loading = document.getElementById("loading");
    const resultCount = document.getElementById("result-count");

    if (!input || !results || !loading || !resultCount) {
        console.error("Required HTML elements not found.");
        return;
    }

    const userRequest = input.value.trim();

    if (!userRequest) {
        input.focus();
        return;
    }


    // Clear previous results

    results.innerHTML = "";
    resultCount.innerHTML = "";


    // Loading

    loading.innerHTML = `
        <div class="ai-loading">

            <div class="loading-spinner"></div>

            <div>
                <strong>OmniAI is thinking...</strong>

                <span>
                    Finding the best real results for you
                </span>
            </div>

        </div>
    `;


    try {

        console.log("=================================");
        console.log("OmniAI request:", userRequest);
        console.log("Sending request to /api/recommend");
        console.log("=================================");


        // =================================================
        // IMPORTANT:
        // Backend route is /api/recommend
        // =================================================

        const response = await fetch("/api/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                request: userRequest
            })

        });


        // Get response

        const data = await response.json();


        console.log("Backend status:", response.status);
        console.log("Backend response:", data);


        // Stop loading

        loading.innerHTML = "";


        // =================================================
        // BACKEND ERROR
        // =================================================

        if (!response.ok) {

            console.error(
                "Backend error:",
                data
            );


            results.innerHTML = `

                <div class="no-results-card">

                    <div class="no-results-icon">
                        ⚠️
                    </div>

                    <h3>
                        OmniAI encountered an error
                    </h3>

                    <p>
                        ${escapeHTML(
                            data.error ||
                            data.message ||
                            "Unable to process your request."
                        )}
                    </p>

                    <button
                        class="retry-button"
                        type="button"
                        onclick="focusSearch()"
                    >
                        Try Again
                    </button>

                </div>

            `;

            return;
        }


        // =================================================
        // NO PRODUCTS
        // =================================================

        if (
            !data.products ||
            data.products.length === 0
        ) {

            console.log(
                "No products returned by backend."
            );


            // Show what OmniAI understood

            let understandingHTML = "";

            if (data.understanding) {

                const understanding =
                    data.understanding;

                understandingHTML = `

                    <div class="understanding-card">

                        <div class="understanding-header">

                            <div class="understanding-icon">
                                ✦
                            </div>

                            <div>

                                <h3>
                                    OmniAI understood your request
                                </h3>

                                <p>
                                    But no real results were found.
                                </p>

                            </div>

                        </div>


                        <div class="understanding-details">

                            <div class="understanding-item">

                                <span>
                                    Category
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        understanding.category ||
                                        "Not specified"
                                    )}
                                </strong>

                            </div>


                            <div class="understanding-item">

                                <span>
                                    Product
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        understanding.product_type ||
                                        "Not specified"
                                    )}
                                </strong>

                            </div>


                            ${
                                understanding.budget
                                ?
                                `

                                <div class="understanding-item">

                                    <span>
                                        Budget
                                    </span>

                                    <strong>
                                        ${escapeHTML(
                                            understanding.budget
                                        )}
                                    </strong>

                                </div>

                                `
                                :
                                ""
                            }

                        </div>

                    </div>

                `;

            }


            results.innerHTML = `

                ${understandingHTML}

                <div class="no-results-card">

                    <div class="no-results-icon">
                        🔍
                    </div>

                    <h3>
                        No real recommendations found
                    </h3>

                    <p>
                        ${
                            escapeHTML(
                                data.message ||
                                "Try another product, budget, brand or preference."
                            )
                        }
                    </p>

                    <button
                        class="retry-button"
                        type="button"
                        onclick="focusSearch()"
                    >
                        Try Again
                    </button>

                </div>

            `;

            return;
        }


        // =================================================
        // RESULT COUNT
        // =================================================

        resultCount.innerHTML = `
            ✨ ${data.products.length} recommendations found
        `;


        // =================================================
        // OMNIAI UNDERSTANDING
        // =================================================

        if (data.understanding) {

            const understanding =
                data.understanding;

            const info =
                document.createElement("div");

            info.className =
                "understanding-card";


            info.innerHTML = `

                <div class="understanding-header">

                    <div class="understanding-icon">
                        ✦
                    </div>

                    <div>

                        <h3>
                            OmniAI understood your request
                        </h3>

                        <p>
                            Here's what our AI identified
                        </p>

                    </div>

                </div>


                <div class="understanding-details">


                    <div class="understanding-item">

                        <span>
                            Category
                        </span>

                        <strong>
                            ${escapeHTML(
                                understanding.category ||
                                "Not specified"
                            )}
                        </strong>

                    </div>


                    <div class="understanding-item">

                        <span>
                            Product
                        </span>

                        <strong>
                            ${escapeHTML(
                                understanding.product_type ||
                                "Not specified"
                            )}
                        </strong>

                    </div>


                    ${
                        understanding.budget
                        ?
                        `

                        <div class="understanding-item">

                            <span>
                                Budget
                            </span>

                            <strong>
                                ${escapeHTML(
                                    understanding.budget
                                )}
                            </strong>

                        </div>

                        `
                        :
                        ""
                    }


                    ${
                        understanding.brand
                        ?
                        `

                        <div class="understanding-item">

                            <span>
                                Brand
                            </span>

                            <strong>
                                ${escapeHTML(
                                    understanding.brand
                                )}
                            </strong>

                        </div>

                        `
                        :
                        ""
                    }


                    ${
                        understanding.platform
                        ?
                        `

                        <div class="understanding-item">

                            <span>
                                Platform
                            </span>

                            <strong>
                                ${escapeHTML(
                                    understanding.platform
                                )}
                            </strong>

                        </div>

                        `
                        :
                        ""
                    }

                </div>

            `;


            results.appendChild(info);

        }


        // =================================================
        // DISPLAY PRODUCTS
        // =================================================

        data.products.forEach(
            (product, index) => {

                const card =
                    document.createElement("article");

                card.className =
                    "product";


                // =================================================
                // RANK
                // =================================================

                const rank = `

                    <div class="product-rank">
                        #${index + 1}
                    </div>

                `;


                // =================================================
                // IMAGE
                // =================================================

                let imageHTML;


                if (product.image) {

                    imageHTML = `

                        <div class="product-image-wrapper">

                            <img

                                src="${escapeAttribute(
                                    product.image
                                )}"

                                alt="${escapeAttribute(
                                    product.title ||
                                    "Recommended product"
                                )}"

                                loading="lazy"

                                onerror="
                                    this.style.display='none';
                                    this.parentElement.classList.add('image-error');
                                "

                            >

                            <div class="image-fallback">
                                🛍️
                            </div>

                        </div>

                    `;

                }

                else {

                    imageHTML = `

                        <div class="product-image-wrapper image-error">

                            <div class="image-fallback">
                                🛍️
                            </div>

                        </div>

                    `;

                }


                // =================================================
                // TITLE
                // =================================================

                const title =
                    product.title ||
                    "Recommended Product";


                // =================================================
                // PRICE
                // =================================================

                const price =
                    product.price ||
                    "Price unavailable";


                // =================================================
                // STORE
                // =================================================

                const store =
                    product.store ||
                    "Platform unavailable";


                // =================================================
                // RATING
                // =================================================

                let ratingHTML;


                if (product.rating) {

                    ratingHTML = `

                        <span class="rating">

                            <span class="star">
                                ★
                            </span>

                            ${escapeHTML(
                                product.rating
                            )}

                        </span>

                    `;

                }

                else {

                    ratingHTML = `

                        <span class="muted">
                            Not available
                        </span>

                    `;

                }


                // =================================================
                // REVIEWS
                // =================================================

                const reviews =
                    product.reviews
                    ?
                    `${product.reviews} reviews`
                    :
                    "No reviews";


                // =================================================
                // PRODUCT LINK
                // =================================================

                let linkHTML = "";


                if (product.link) {

                    linkHTML = `

                        <a

                            class="product-button"

                            href="${escapeAttribute(
                                product.link
                            )}"

                            target="_blank"

                            rel="noopener noreferrer"

                        >

                            View Product

                            <span>
                                →
                            </span>

                        </a>

                    `;

                }


                // =================================================
                // PRODUCT CARD
                // =================================================

                card.innerHTML = `

                    ${rank}

                    ${imageHTML}


                    <div class="product-content">


                        <h3 class="product-title">

                            ${escapeHTML(title)}

                        </h3>


                        <div class="product-price">

                            ${escapeHTML(price)}

                        </div>


                        <div class="product-info">


                            <div class="info-row">

                                <span>
                                    Store
                                </span>

                                <strong>
                                    ${escapeHTML(store)}
                                </strong>

                            </div>


                            <div class="info-row">

                                <span>
                                    Rating
                                </span>

                                ${ratingHTML}

                            </div>


                            <div class="info-row">

                                <span>
                                    Reviews
                                </span>

                                <strong>
                                    ${escapeHTML(reviews)}
                                </strong>

                            </div>


                        </div>


                        ${linkHTML}


                    </div>

                `;


                results.appendChild(card);

            }
        );


        // =================================================
        // SCROLL TO RESULTS
        // =================================================

        const resultsSection =
            document.querySelector(
                ".results-section"
            );


        if (resultsSection) {

            setTimeout(() => {

                resultsSection.scrollIntoView({

                    behavior: "smooth",

                    block: "start"

                });

            }, 150);

        }

    }


    // =================================================
    // FRONTEND ERROR
    // =================================================

    catch (error) {

        console.error(
            "❌ OmniAI request failed:",
            error
        );


        loading.innerHTML = "";

        resultCount.innerHTML = "";


        results.innerHTML = `

            <div class="no-results-card">

                <div class="no-results-icon">
                    ⚠️
                </div>

                <h3>
                    Connection error
                </h3>

                <p>
                    OmniAI could not connect to the backend.
                    Please make sure Flask is running.
                </p>

                <button
                    class="retry-button"
                    type="button"
                    onclick="focusSearch()"
                >

                    Try Again

                </button>

            </div>

        `;

    }

}


// =====================================================
// VOICE INPUT
// =====================================================

let omniAIRecognition = null;

let isListening = false;


// =====================================================
// START VOICE INPUT
// =====================================================

function startVoiceInput() {

    console.log(
        "🎤 Microphone button clicked"
    );


    const input =
        document.getElementById(
            "userRequest"
        );

    const micButton =
        document.getElementById(
            "micButton"
        );

    const voiceStatus =
        document.getElementById(
            "voiceStatus"
        );

    const languageSelect =
        document.getElementById(
            "languageSelect"
        );


    if (!input) {

        console.error(
            "❌ userRequest textarea not found"
        );

        return;

    }


    // =================================================
    // BROWSER SUPPORT
    // =================================================

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        if (voiceStatus) {

            voiceStatus.textContent =
                "❌ Voice input is not supported. Please use Google Chrome.";

        }

        return;

    }


    // =================================================
    // STOP CURRENT RECOGNITION
    // =================================================

    if (
        isListening &&
        omniAIRecognition
    ) {

        omniAIRecognition.stop();

        return;

    }


    // =================================================
    // CREATE RECOGNITION
    // =================================================

    omniAIRecognition =
        new SpeechRecognition();


    // =================================================
    // LANGUAGE
    // =================================================

    const selectedLanguage =
        languageSelect
        ?
        languageSelect.value
        :
        "en-IN";


    omniAIRecognition.lang =
        selectedLanguage ||
        "en-IN";


    // =================================================
    // SETTINGS
    // =================================================

    omniAIRecognition.continuous =
        false;

    omniAIRecognition.interimResults =
        true;

    omniAIRecognition.maxAlternatives =
        1;


    // =================================================
    // START
    // =================================================

    omniAIRecognition.onstart =
        function () {

            console.log(
                "🎙️ Voice recognition started"
            );


            isListening = true;


            if (micButton) {

                micButton.classList.add(
                    "listening"
                );

                micButton.setAttribute(
                    "aria-label",
                    "Stop voice input"
                );

            }


            if (voiceStatus) {

                voiceStatus.textContent =
                    "🎙️ Listening... Speak now";

            }

        };


    // =================================================
    // RESULT
    // =================================================

    omniAIRecognition.onresult =
        function (event) {

            console.log(
                "🗣️ Speech result received"
            );


            let transcript = "";


            for (
                let i = event.resultIndex;
                i < event.results.length;
                i++
            ) {

                transcript +=
                    event.results[i][0]
                        .transcript;

            }


            transcript =
                transcript.trim();


            console.log(
                "📝 Transcript:",
                transcript
            );


            if (transcript !== "") {

                input.value =
                    transcript;


                input.dispatchEvent(
                    new Event(
                        "input",
                        {
                            bubbles: true
                        }
                    )
                );


                input.focus();


                input.setSelectionRange(
                    input.value.length,
                    input.value.length
                );


                if (voiceStatus) {

                    voiceStatus.textContent =
                        "✍️ " + transcript;

                }

            }

        };


    // =================================================
    // END
    // =================================================

    omniAIRecognition.onend =
        function () {

            console.log(
                "🛑 Voice recognition ended"
            );


            isListening = false;


            if (micButton) {

                micButton.classList.remove(
                    "listening"
                );

                micButton.setAttribute(
                    "aria-label",
                    "Start voice input"
                );

            }


            if (input.value.trim()) {

                if (voiceStatus) {

                    voiceStatus.textContent =
                        "✅ Speech added to search box";

                }

            }

            else {

                if (voiceStatus) {

                    voiceStatus.textContent =
                        "🎤 No speech detected. Click microphone and try again.";

                }

            }

        };


    // =================================================
    // ERROR
    // =================================================

    omniAIRecognition.onerror =
        function (event) {

            console.error(
                "❌ Speech recognition error:",
                event.error
            );


            isListening = false;


            if (micButton) {

                micButton.classList.remove(
                    "listening"
                );

                micButton.setAttribute(
                    "aria-label",
                    "Start voice input"
                );

            }


            if (!voiceStatus) {
                return;
            }


            switch (event.error) {

                case "not-allowed":

                    voiceStatus.textContent =
                        "🎤 Microphone permission denied. Allow microphone access in Chrome.";

                    break;


                case "no-speech":

                    voiceStatus.textContent =
                        "🔊 No speech detected. Speak clearly and try again.";

                    break;


                case "audio-capture":

                    voiceStatus.textContent =
                        "🎤 Microphone not found. Check your microphone.";

                    break;


                case "network":

                    voiceStatus.textContent =
                        "🌐 Voice recognition network error. Check your internet connection.";

                    break;


                case "aborted":

                    voiceStatus.textContent =
                        "🛑 Voice input stopped.";

                    break;


                default:

                    voiceStatus.textContent =
                        "❌ Voice input error: " +
                        event.error;

            }

        };


    // =================================================
    // START MICROPHONE
    // =================================================

    try {

        console.log(
            "🎤 Starting microphone..."
        );


        omniAIRecognition.start();

    }

    catch (error) {

        console.error(
            "❌ Could not start microphone:",
            error
        );


        isListening = false;

    }

}


// =====================================================
// KEYBOARD SEARCH
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const input =
            document.getElementById(
                "userRequest"
            );


        if (!input) {
            return;
        }


        input.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();

                    getRecommendations();

                }

            }
        );

    }
);


// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHTML(value) {

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


// =====================================================
// ATTRIBUTE ESCAPE
// =====================================================

function escapeAttribute(value) {

    return escapeHTML(value);

}
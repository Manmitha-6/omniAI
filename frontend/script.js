// ============================================================
// OMNIAI - FRONTEND JAVASCRIPT
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("🚀 OmniAI frontend starting...");

    // ============================================================
    // GET ELEMENTS
    // ============================================================

    const loginScreen = document.getElementById("loginScreen");
    const appScreen = document.getElementById("appScreen");
    const loginInput = document.getElementById("loginInput");
    const continueBtn = document.getElementById("continueBtn");
    const welcomeName = document.getElementById("welcomeName");
    const profileName = document.getElementById("profileName");
    const logoutBtn = document.getElementById("logoutBtn");
    const userRequest = document.getElementById("userRequest");
    const searchButton = document.getElementById("searchButton");
    const micButton = document.getElementById("micButton");
    const minPrice = document.getElementById("minPrice");
    const maxPrice = document.getElementById("maxPrice");
    const applyBudgetBtn = document.getElementById("applyBudgetBtn");
    const loading = document.getElementById("loading");
    const resultsSection = document.getElementById("results-section");
    const resultsContainer = document.getElementById("resultsContainer");
    const themeToggle = document.getElementById("themeToggle");
    const settingsThemeBtn = document.getElementById("settingsThemeBtn");
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const clearDataBtn = document.getElementById("clearDataBtn");
    const voiceSupportStatus =
        document.getElementById("voiceSupportStatus");

    // ============================================================
    // DEBUG - CHECK IMPORTANT ELEMENTS
    // ============================================================

    console.log(
        "🔍 Search button:",
        searchButton ? "FOUND" : "NOT FOUND"
    );

    console.log(
        "🎤 Microphone button:",
        micButton ? "FOUND" : "NOT FOUND"
    );

    console.log(
        "📝 Search input:",
        userRequest ? "FOUND" : "NOT FOUND"
    );

    // ============================================================
    // LOGIN SYSTEM
    // ============================================================

    function isValidEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    function isValidMobile(value) {
        let cleaned = value
            .replace(/\s+/g, "")
            .replace(/-/g, "");

        if (cleaned.startsWith("+91")) {
            cleaned = cleaned.substring(3);
        }

        if (cleaned.startsWith("91") && cleaned.length === 12) {
            cleaned = cleaned.substring(2);
        }

        return /^[6-9]\d{9}$/.test(cleaned);
    }

    // ============================================================
    // ADDED: GET DISPLAY NAME FROM EMAIL
    // ============================================================

    function getUserName(value) {
        value = value.trim();

        if (value.includes("@")) {

            let username = value
                .split("@")[0]
                .replace(/[._-]+/g, " ")
                .replace(/[0-9]/g, "")
                .trim();

            if (!username) {
                return "OmniAI User";
            }

            return username
                .split(/\s+/)
                .filter(Boolean)
                .map(function (word) {
                    return (
                        word.charAt(0).toUpperCase() +
                        word.slice(1).toLowerCase()
                    );
                })
                .join(" ");
        }

        return "OmniAI User";
    }

    function showLoginError(message) {
        if (!loginInput) {
            alert(message);
            return;
        }

        loginInput.style.borderColor = "#ff4f8b";

        let error =
            document.getElementById("loginError");

        if (!error) {
            error = document.createElement("div");
            error.id = "loginError";
            error.style.color = "#ff4f8b";
            error.style.fontSize = "13px";
            error.style.marginTop = "8px";
            error.style.fontWeight = "600";

            if (loginInput.parentElement) {
                loginInput.parentElement.appendChild(error);
            }
        }

        error.textContent = message;
        loginInput.focus();
    }

    function clearLoginError() {
        if (!loginInput) return;

        loginInput.style.borderColor = "";

        const error =
            document.getElementById("loginError");

        if (error) {
            error.remove();
        }
    }

    function login() {

        if (!loginInput) return;

        const value =
            loginInput.value.trim();

        clearLoginError();

        if (!value) {
            showLoginError(
                "Please enter your email or mobile number."
            );
            return;
        }

        const validEmail =
            isValidEmail(value);

        const validMobile =
            isValidMobile(value);

        if (!validEmail && !validMobile) {
            showLoginError(
                "Enter a valid email address or Indian mobile number."
            );
            return;
        }

        const username =
            getUserName(value);

        const user = {
            login: value,
            name: username,
            loginTime:
                new Date().toISOString()
        };

        localStorage.setItem(
            "omniaiUser",
            JSON.stringify(user)
        );

        if (welcomeName) {
            welcomeName.textContent = username;
        }

        if (profileName) {
            profileName.textContent = username;
        }

        // ========================================================
        // ADDED: UPDATE HERO NAME
        // ========================================================

        const heroUserName =
            document.getElementById("heroUserName");

        if (heroUserName) {
            heroUserName.textContent = username;
        }

        // ========================================================
        // ADDED: UPDATE USER AVATAR
        // ========================================================

        const userAvatar =
            document.querySelector(".user-avatar");

        if (userAvatar) {
            userAvatar.textContent =
                username.charAt(0).toUpperCase();
        }

        if (loginScreen) {
            loginScreen.classList.add("hidden");
        }

        if (appScreen) {
            appScreen.classList.remove("hidden");
        }

        setTimeout(function () {

            if (userRequest) {
                userRequest.focus();
            }

        }, 300);

        console.log(
            "✅ Login successful:",
            username
        );
    }

    if (continueBtn) {

        continueBtn.addEventListener(
            "click",
            login
        );
    }

    if (loginInput) {

        loginInput.addEventListener(
            "keydown",
            function (event) {

                if (event.key === "Enter") {

                    event.preventDefault();

                    login();
                }
            }
        );
    }

    // ============================================================
    // RESTORE LOGIN
    // ============================================================

    function restoreUser() {

        const savedUser =
            localStorage.getItem("omniaiUser");

        if (!savedUser) return;

        try {

            const user =
                JSON.parse(savedUser);

            if (!user || !user.name) {
                return;
            }

            if (welcomeName) {
                welcomeName.textContent =
                    user.name;
            }

            if (profileName) {
                profileName.textContent =
                    user.name;
            }

            // ====================================================
            // ADDED: RESTORE HERO NAME
            // ====================================================

            const heroUserName =
                document.getElementById("heroUserName");

            if (heroUserName) {
                heroUserName.textContent =
                    user.name;
            }

            // ====================================================
            // ADDED: RESTORE AVATAR
            // ====================================================

            const userAvatar =
                document.querySelector(".user-avatar");

            if (userAvatar) {
                userAvatar.textContent =
                    user.name.charAt(0).toUpperCase();
            }

            if (loginScreen) {
                loginScreen.classList.add("hidden");
            }

            if (appScreen) {
                appScreen.classList.remove("hidden");
            }

            console.log(
                "✅ User restored:",
                user.name
            );

        }
        catch (error) {

            console.error(
                "Login restore error:",
                error
            );

            localStorage.removeItem(
                "omniaiUser"
            );
        }
    }

    restoreUser();

    // ============================================================
    // LOGOUT
    // ============================================================

    if (logoutBtn) {

        logoutBtn.addEventListener(
            "click",
            function () {

                localStorage.removeItem(
                    "omniaiUser"
                );

                location.reload();
            }
        );
    }

    // ============================================================
    // SOCIAL LOGIN DEMO
    // ============================================================

    const googleLoginBtn =
        document.getElementById("googleLoginBtn");

    const githubLoginBtn =
        document.getElementById("githubLoginBtn");

    function socialLoginDemo() {

        alert(
            "Social login is currently a demo. Please use your email or mobile number."
        );
    }

    if (googleLoginBtn) {

        googleLoginBtn.addEventListener(
            "click",
            socialLoginDemo
        );
    }

    if (githubLoginBtn) {

        githubLoginBtn.addEventListener(
            "click",
            socialLoginDemo
        );
    }

    // ============================================================
    // EXAMPLE SEARCHES
    // ============================================================

    window.setExample = function (category) {

        if (!userRequest) return;

        let text = "";

        if (category === "fashion") {

            text =
                "I want a stylish birthday dress under ₹2000 from Myntra";

        }

        else if (category === "food") {

            text =
                "I want spicy food under ₹300 in Hyderabad";

        }

        else if (category === "electronics") {

            text =
                "I want wireless earbuds under ₹3000";
        }

        userRequest.value = text;
        userRequest.focus();
    };

    // ============================================================
    // QUICK SEARCH
    // ============================================================

    window.quickSearch = function (text) {

        if (!userRequest) return;

        userRequest.value = text;
        userRequest.focus();
    };

    // ============================================================
    // NAVIGATION
    // ============================================================

    const pageButtons =
        document.querySelectorAll("[data-page]");

    const pages =
        document.querySelectorAll(".page");

    pageButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const pageId =
                    button.getAttribute("data-page");

                pages.forEach(function (page) {

                    page.classList.add("hidden");
                });

                const selectedPage =
                    document.getElementById(pageId);

                if (selectedPage) {

                    selectedPage.classList.remove(
                        "hidden"
                    );

                    selectedPage.classList.add(
                        "active-page"
                    );
                }

                document.body.classList.remove(
                    "sidebar-open"
                );
            }
        );
    });

    window.goHome = function () {

        pages.forEach(function (page) {

            page.classList.add("hidden");
        });

        const home =
            document.getElementById("homePage");

        if (home) {

            home.classList.remove("hidden");
        }

        if (resultsSection) {

            resultsSection.classList.add(
                "hidden"
            );
        }

        window.scrollTo({

            top: 0,
            behavior: "smooth"

        });
    };

    // ============================================================
    // MOBILE MENU
    // ============================================================

    if (mobileMenuBtn) {

        mobileMenuBtn.addEventListener(
            "click",
            function () {

                document.body.classList.toggle(
                    "sidebar-open"
                );
            }
        );
    }

    // ============================================================
    // APPLY BUDGET
    // ============================================================

    if (applyBudgetBtn) {

        applyBudgetBtn.addEventListener(
            "click",
            function () {

                if (userRequest) {
                    userRequest.focus();
                }
            }
        );
    }

    // ============================================================
    // SEARCH
    // ============================================================

    async function getRecommendations() {

        if (!userRequest) {

            console.error(
                "❌ userRequest not found."
            );

            return;
        }

        const request =
            userRequest.value.trim();

        if (!request) {

            alert(
                "Please tell OmniAI what you are looking for."
            );

            userRequest.focus();

            return;
        }

        // --------------------------------------------------------
        // SHOW LOADING
        // --------------------------------------------------------

        if (loading) {

            loading.classList.remove(
                "hidden"
            );
        }

        if (resultsSection) {

            resultsSection.classList.add(
                "hidden"
            );
        }

        if (resultsContainer) {

            resultsContainer.innerHTML = "";
        }

        if (searchButton) {

            searchButton.disabled = true;

            searchButton.textContent =
                "✨ Finding...";
        }

        try {

            console.log(
                "🔍 Sending request:",
                request
            );

            // ----------------------------------------------------
            // API REQUEST
            // ----------------------------------------------------

            const response =
                await fetch(
                    "/api/recommend",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            request: request,

                            min_price:
                                minPrice &&
                                minPrice.value
                                    ? Number(
                                        minPrice.value
                                    )
                                    : null,

                            max_price:
                                maxPrice &&
                                maxPrice.value
                                    ? Number(
                                        maxPrice.value
                                    )
                                    : null
                        })
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Server returned HTTP " +
                    response.status
                );
            }

            const data =
                await response.json();

            console.log(
                "📦 OmniAI response:",
                data
            );

            // ----------------------------------------------------
            // GET PRODUCTS
            // ----------------------------------------------------

            let products = [];

            if (Array.isArray(data)) {

                products = data;
            }

            else if (
                Array.isArray(data.products)
            ) {

                products =
                    data.products;
            }

            else if (
                Array.isArray(data.recommendations)
            ) {

                products =
                    data.recommendations;
            }

            else if (
                Array.isArray(data.results)
            ) {

                products =
                    data.results;
            }

            else if (
                data.data &&
                Array.isArray(data.data.products)
            ) {

                products =
                    data.data.products;
            }

            // ----------------------------------------------------
            // ERROR FROM BACKEND
            // ----------------------------------------------------

            if (data.error) {

                showError(
                    data.error
                );

                return;
            }

            if (!products.length) {

                showEmptyState();

                return;
            }

            // ----------------------------------------------------
            // SAVE HISTORY
            // ----------------------------------------------------

            saveSearchHistory(
                request
            );

            // ----------------------------------------------------
            // DISPLAY RESULTS
            // ----------------------------------------------------

            renderProducts(products);

        }

        catch (error) {

            console.error(
                "❌ Recommendation error:",
                error
            );

            showError(
                "OmniAI could not get recommendations right now. Please try again."
            );
        }

        finally {

            if (loading) {

                loading.classList.add(
                    "hidden"
                );
            }

            if (searchButton) {

                searchButton.disabled = false;

                searchButton.textContent =
                    "🔍 Find Recommendations";
            }
        }
    }

    // ============================================================
    // SEARCH BUTTON
    // ============================================================

    if (searchButton) {

        searchButton.addEventListener(
            "click",
            getRecommendations
        );

        console.log(
            "✅ Search button connected."
        );

    }

    else {

        console.error(
            "❌ searchButton not found."
        );
    }

    // ============================================================
    // ENTER TO SEARCH
    // ============================================================

    if (userRequest) {

        userRequest.addEventListener(
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

    // ============================================================
    // RENDER PRODUCTS
    // ============================================================

    function renderProducts(products) {

        if (!resultsContainer) {

            console.error(
                "❌ resultsContainer not found."
            );

            return;
        }

        resultsContainer.innerHTML = "";

        products.forEach(
            function (product, index) {

                // ------------------------------------------------
                // BASIC PRODUCT INFORMATION
                // ------------------------------------------------

                const title =
                    product.title ||
                    product.name ||
                    product.product_name ||
                    "Recommended Product";

                const price =
                    product.price ??
                    product.cost ??
                    product.amount ??
                    "Price unavailable";

                const image =
                    product.image ||
                    product.thumbnail ||
                    product.image_url ||
                    "";

                const link =
                    product.product_link ||
                    product.product_url ||
                    product.link ||
                    "#";

                const source =
                    product.source ||
                    product.store ||
                    product.platform ||
                    "Online Store";

                const rating =
                    product.rating ??
                    "";

                const reviews =
                    product.reviews ??
                    "";

                const category =
                    product.category ||
                    "Recommendation";

                const description =
                    product.description ||
                    "Recommended by OmniAI based on your requirements.";

                // ------------------------------------------------
                // ADDRESS INFORMATION
                // ------------------------------------------------

                const address =
                    product.address ||
                    product.formatted_address ||
                    product.location ||
                    "";

                // ------------------------------------------------
                // DETECT LOCAL / RESTAURANT RESULT
                // ------------------------------------------------

                const sourceText =
                    String(source).toLowerCase();

                const categoryText =
                    String(category).toLowerCase();

                const titleText =
                    String(title).toLowerCase();

                const isLocal =
                    sourceText.includes("google local") ||
                    sourceText.includes("local") ||
                    categoryText.includes("restaurant") ||
                    categoryText.includes("food") ||
                    titleText.includes("pizzeria") ||
                    titleText.includes("pizza") ||
                    titleText.includes("restaurant") ||
                    titleText.includes("cafe") ||
                    titleText.includes("café") ||
                    titleText.includes("bakery") ||
                    !!address;

                // ------------------------------------------------
                // CREATE CARD
                // ------------------------------------------------

                const card =
                    document.createElement("article");

                card.className =
                    "product-card";

                // ------------------------------------------------
                // IMAGE HTML
                // ------------------------------------------------

                let imageHTML = "";

                if (image) {

                    imageHTML = `
                        <img
                            class="product-image"
                            src="${escapeHtml(image)}"
                            alt="${escapeHtml(title)}"
                            onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                        >
                        <div
                            class="product-placeholder"
                            style="display:none;"
                        >
                            ✨
                        </div>
                    `;
                }

                else {

                    imageHTML = `
                        <div class="product-placeholder">
                            ✨
                        </div>
                    `;
                }

                // ------------------------------------------------
                // RESULT ACTION BUTTON
                // ------------------------------------------------

                let actionHTML = "";

                if (isLocal) {

                    let addressLink =
                        product.maps_link ||
                        product.google_maps_url ||
                        product.directions_link ||
                        "";

                    if (!addressLink && link !== "#") {

                        addressLink = link;
                    }

                    if (!addressLink && address) {

                        addressLink =
                            "https://www.google.com/maps/search/?api=1&query=" +
                            encodeURIComponent(
                                title + " " + address
                            );
                    }

                    if (addressLink) {

                        actionHTML = `
                            <a
                                class="view-product-btn"
                                href="${escapeHtml(addressLink)}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                📍 View Address →
                            </a>
                        `;
                    }

                    else {

                        actionHTML = `
                            <button
                                type="button"
                                class="view-product-btn"
                                disabled
                            >
                                📍 Address Unavailable
                            </button>
                        `;
                    }

                }

                else {

                    // ------------------------------------------------
                    // NORMAL PRODUCT
                    // ------------------------------------------------

                    if (link && link !== "#") {

                        actionHTML = `
                            <a
                                class="view-product-btn"
                                href="${escapeHtml(link)}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                View Product →
                            </a>
                        `;
                    }

                    else {

                        actionHTML = `
                            <button
                                type="button"
                                class="view-product-btn"
                                disabled
                            >
                                Product Link Unavailable
                            </button>
                        `;
                    }
                }

                // ------------------------------------------------
                // CARD HTML
                // ------------------------------------------------

                card.innerHTML = `
                    <div class="product-image-wrapper">

                        ${imageHTML}

                        <div class="recommendation-number">
                            #${index + 1}
                        </div>

                        <button
                            type="button"
                            class="save-product-btn"
                            aria-label="Save product"
                        >
                            ♡
                        </button>

                    </div>

                    <div class="product-content">

                        <div class="product-category">
                            ${escapeHtml(category)}
                        </div>

                        <h3 class="product-title">
                            ${escapeHtml(title)}
                        </h3>

                        <p class="product-description">
                            ${escapeHtml(description)}
                        </p>

                        <div class="product-price">

                            ${
                                typeof price === "number"
                                    ? "₹" +
                                      price.toLocaleString("en-IN")
                                    : escapeHtml(String(price))
                            }

                        </div>

                        <div class="product-source">
                            🛍️ ${escapeHtml(String(source))}
                        </div>

                        ${
                            rating
                                ? `
                                    <div class="product-rating">

                                        ⭐ ${escapeHtml(String(rating))}

                                        ${
                                            reviews
                                                ? " (" +
                                                  escapeHtml(
                                                      String(reviews)
                                                  ) +
                                                  " reviews)"
                                                : ""
                                        }

                                    </div>
                                  `
                                : ""
                        }

                        ${actionHTML}

                    </div>
                `;

                // ------------------------------------------------
                // SAVE BUTTON
                // ------------------------------------------------

                const saveButton =
                    card.querySelector(
                        ".save-product-btn"
                    );

                if (saveButton) {

                    saveButton.addEventListener(
                        "click",
                        function () {

                            saveProduct(product);

                            saveButton.classList.toggle(
                                "saved"
                            );

                            saveButton.textContent =
                                saveButton.classList.contains(
                                    "saved"
                                )
                                    ? "♥"
                                    : "♡";
                        }
                    );
                }

                resultsContainer.appendChild(
                    card
                );
            }
        );

        if (resultsSection) {

            resultsSection.classList.remove(
                "hidden"
            );

            resultsSection.scrollIntoView({

                behavior: "smooth",
                block: "start"

            });
        }

        console.log(
            "✅ Displayed",
            products.length,
            "recommendations."
        );
    }

    // ============================================================
    // ESCAPE HTML
    // ============================================================

    function escapeHtml(value) {

        return String(value)

            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // ============================================================
    // EMPTY STATE
    // ============================================================

    function showEmptyState() {

        if (!resultsContainer) return;

        resultsContainer.innerHTML = `

            <div class="omniai-empty-state">

                <h2>
                    🔎 No recommendations found
                </h2>

                <p>
                    Try changing your search,
                    budget or category.
                </p>

            </div>
        `;

        if (resultsSection) {

            resultsSection.classList.remove(
                "hidden"
            );
        }
    }

    // ============================================================
    // ERROR STATE
    // ============================================================

    function showError(message) {

        if (!resultsContainer) return;

        resultsContainer.innerHTML = `

            <div class="omniai-error-state">

                <h2>
                    ⚠️ OmniAI needs another try
                </h2>

                <p>
                    ${escapeHtml(message)}
                </p>

                <button
                    type="button"
                    id="retrySearchBtn"
                >
                    Try Again
                </button>

            </div>
        `;

        if (resultsSection) {

            resultsSection.classList.remove(
                "hidden"
            );
        }

        const retryButton =
            document.getElementById(
                "retrySearchBtn"
            );

        if (retryButton) {

            retryButton.addEventListener(
                "click",
                getRecommendations
            );
        }
    }

    // ============================================================
    // HISTORY
    // ============================================================

    function getCurrentUserKey() {

        const savedUser =
            localStorage.getItem("omniaiUser");

        if (!savedUser) {

            return "guest";
        }

        try {

            const user =
                JSON.parse(savedUser);

            return (
                user.login ||
                user.name ||
                "guest"
            );
        }

        catch {

            return "guest";
        }
    }

    function saveSearchHistory(request) {

        const key =
            "omniai_history_" +
            getCurrentUserKey();

        let history = [];

        try {

            history =
                JSON.parse(
                    localStorage.getItem(key)
                ) || [];
        }

        catch {

            history = [];
        }

        history.unshift({

            request: request,

            time:
                new Date().toISOString()
        });

        history =
            history.slice(0, 30);

        localStorage.setItem(
            key,
            JSON.stringify(history)
        );
    }

    // ============================================================
    // SAVE PRODUCTS
    // ============================================================

    function saveProduct(product) {

        const key =
            "omniai_saved_" +
            getCurrentUserKey();

        let saved = [];

        try {

            saved =
                JSON.parse(
                    localStorage.getItem(key)
                ) || [];
        }

        catch {

            saved = [];
        }

        saved.push(product);

        localStorage.setItem(
            key,
            JSON.stringify(saved)
        );

        console.log(
            "❤️ Product saved."
        );
    }

    // ============================================================
    // VOICE SEARCH
    // ============================================================

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (voiceSupportStatus) {

        voiceSupportStatus.textContent =
            SpeechRecognition
                ? "Available"
                : "Not supported";
    }

    if (micButton) {

        if (!SpeechRecognition) {

            micButton.addEventListener(
                "click",
                function () {

                    alert(
                        "Voice search is not supported in this browser. Please use Google Chrome or Microsoft Edge."
                    );
                }
            );

        }

        else {

            const recognition =
                new SpeechRecognition();

            recognition.lang =
                "en-IN";

            recognition.continuous =
                false;

            recognition.interimResults =
                true;

            recognition.onstart =
                function () {

                    micButton.classList.add(
                        "listening"
                    );

                    micButton.textContent =
                        "🔴";

                    console.log(
                        "🎤 Listening..."
                    );
                };

            recognition.onresult =
                function (event) {

                    let transcript = "";

                    for (
                        let i =
                            event.resultIndex;

                        i <
                            event.results.length;

                        i++
                    ) {

                        transcript +=
                            event.results[i][0]
                                .transcript;
                    }

                    if (userRequest) {

                        userRequest.value =
                            transcript;
                    }
                };

            recognition.onend =
                function () {

                    micButton.classList.remove(
                        "listening"
                    );

                    micButton.textContent =
                        "🎤";

                    console.log(
                        "🎤 Voice input finished."
                    );
                };

            recognition.onerror =
                function (event) {

                    micButton.classList.remove(
                        "listening"
                    );

                    micButton.textContent =
                        "🎤";

                    console.error(
                        "Voice error:",
                        event.error
                    );
                };

            micButton.addEventListener(
                "click",
                function () {

                    try {

                        recognition.start();

                    }

                    catch (error) {

                        console.log(
                            "Voice recognition already running."
                        );
                    }
                }
            );
        }

        console.log(
            "🎤 Microphone button connected."
        );

    }

    else {

        console.error(
            "❌ micButton not found."
        );
    }

    // ============================================================
    // THEME
    // ============================================================

    function toggleTheme() {

        document.body.classList.toggle(
            "dark-mode"
        );

        const isDark =
            document.body.classList.contains(
                "dark-mode"
            );

        localStorage.setItem(
            "omniaiTheme",
            isDark
                ? "dark"
                : "light"
        );
    }

    if (themeToggle) {

        themeToggle.addEventListener(
            "click",
            toggleTheme
        );
    }

    if (settingsThemeBtn) {

        settingsThemeBtn.addEventListener(
            "click",
            toggleTheme
        );
    }

    const savedTheme =
        localStorage.getItem(
            "omniaiTheme"
        );

    if (savedTheme === "dark") {

        document.body.classList.add(
            "dark-mode"
        );
    }

    // ============================================================
    // CLEAR DATA
    // ============================================================

    if (clearDataBtn) {

        clearDataBtn.addEventListener(
            "click",
            function () {

                const confirmed =
                    confirm(
                        "Clear your OmniAI saved data and history?"
                    );

                if (!confirmed) return;

                const userKey =
                    getCurrentUserKey();

                localStorage.removeItem(
                    "omniai_history_" +
                    userKey
                );

                localStorage.removeItem(
                    "omniai_saved_" +
                    userKey
                );

                alert(
                    "✅ OmniAI saved data and history cleared."
                );
            }
        );
    }

    // ============================================================
    // GLOBAL FUNCTIONS
    // ============================================================

    window.getRecommendations =
        getRecommendations;

    window.startVoiceInput =
        function () {

            if (micButton) {

                micButton.click();
            }
        };

    // ============================================================
    // FINAL STATUS
    // ============================================================

    console.log(
        "✨ OmniAI frontend loaded successfully."
    );

    console.log(
        "🎤 Voice support:",
        SpeechRecognition
            ? "Available"
            : "Not supported"
    );

    console.log(
        "🔍 Search button:",
        searchButton
            ? "FOUND"
            : "NOT FOUND"
    );

    console.log(
        "🎤 Microphone button:",
        micButton
            ? "FOUND"
            : "NOT FOUND"
    );

    console.log(
        "📝 Search input:",
        userRequest
            ? "FOUND"
            : "NOT FOUND"
    );

});
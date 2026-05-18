/**
 * HouseAI — Frontend interactions
 * Form validation, loading states, and prediction API calls
 */

(function () {
    "use strict";

    const form = document.getElementById("prediction-form");
    const predictBtn = document.getElementById("predict-btn");
    const resetBtn = document.getElementById("reset-btn");

    const loadingState = document.getElementById("loading-state");
    const placeholderState = document.getElementById("placeholder-state");
    const resultState = document.getElementById("result-state");
    const errorState = document.getElementById("error-state");

    const predictedPriceEl = document.getElementById("predicted-price");
    const resultSummaryEl = document.getElementById("result-summary");
    const errorMessageEl = document.getElementById("error-message");

    /** Field validation rules (min, max) */
    const FIELD_RULES = {
        OverallQual: { min: 1, max: 10, label: "Overall Quality" },
        GrLivArea: { min: 300, max: 10000, label: "Living Area" },
        GarageCars: { min: 0, max: 4, label: "Garage Cars" },
        TotalBsmtSF: { min: 0, max: 6000, label: "Basement SF" },
        FullBath: { min: 0, max: 5, label: "Full Baths" },
        YearBuilt: { min: 1872, max: 2026, label: "Year Built" },
    };

    const FIELD_LABELS = {
        OverallQual: "Overall Quality",
        GrLivArea: "Living Area (sq ft)",
        GarageCars: "Garage Cars",
        TotalBsmtSF: "Basement (sq ft)",
        FullBath: "Full Baths",
        YearBuilt: "Year Built",
    };

    /**
     * Show only the given panel; hide others
     */
    function showPanel(panel) {
        [placeholderState, loadingState, resultState, errorState].forEach((el) => {
            el.classList.add("hidden");
        });
        if (panel) {
            panel.classList.remove("hidden");
        }
    }

    /**
     * Validate a single input against rules
     */
    function validateField(input) {
        const name = input.name;
        const rules = FIELD_RULES[name];
        if (!rules) return true;

        const value = input.value.trim();
        if (value === "") {
            input.classList.add("invalid");
            return { valid: false, message: `${rules.label} is required.` };
        }

        const num = Number(value);
        if (Number.isNaN(num)) {
            input.classList.add("invalid");
            return { valid: false, message: `${rules.label} must be a number.` };
        }

        if (num < rules.min || num > rules.max) {
            input.classList.add("invalid");
            return {
                valid: false,
                message: `${rules.label} must be between ${rules.min} and ${rules.max}.`,
            };
        }

        input.classList.remove("invalid");
        return { valid: true };
    }

    /**
     * Validate entire form
     */
    function validateForm() {
        const inputs = form.querySelectorAll("input[name]");
        let firstError = null;

        inputs.forEach((input) => {
            const result = validateField(input);
            if (!result.valid && !firstError) {
                firstError = result.message;
            }
        });

        return firstError;
    }

    /**
     * Collect form data as plain object for API
     */
    function getFormData() {
        const data = {};
        const inputs = form.querySelectorAll("input[name]");
        inputs.forEach((input) => {
            data[input.name] = input.value.trim();
        });
        return data;
    }

    /**
     * Set button loading state
     */
    function setLoading(isLoading) {
        predictBtn.disabled = isLoading;
        predictBtn.classList.toggle("loading", isLoading);
        if (isLoading) {
            predictBtn.querySelector(".btn-text").textContent = "Predicting…";
        } else {
            predictBtn.querySelector(".btn-text").textContent = "Predict Price";
        }
    }

    /**
     * Render prediction result summary
     */
    function renderSummary(inputs) {
        resultSummaryEl.innerHTML = "";
        Object.keys(FIELD_LABELS).forEach((key) => {
            const li = document.createElement("li");
            const label = document.createElement("span");
            label.textContent = FIELD_LABELS[key];
            const value = document.createElement("span");
            value.textContent = inputs[key] ?? "—";
            li.appendChild(label);
            li.appendChild(value);
            resultSummaryEl.appendChild(li);
        });
    }

    /**
     * Call Flask /predict endpoint
     */
    async function fetchPrediction(data) {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify(data),
        });

        const payload = await response.json();
        if (!response.ok || !payload.success) {
            throw new Error(payload.error || "Prediction failed.");
        }
        return payload;
    }

    /**
     * Handle form submit
     */
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const error = validateForm();
        if (error) {
            showPanel(errorState);
            errorMessageEl.textContent = error;
            return;
        }

        const data = getFormData();
        setLoading(true);
        showPanel(loadingState);

        try {
            const result = await fetchPrediction(data);
            predictedPriceEl.textContent = result.formatted_price;
            renderSummary(result.inputs || data);
            showPanel(resultState);
        } catch (err) {
            showPanel(errorState);
            errorMessageEl.textContent =
                err.message || "Unable to connect to the server. Is Flask running?";
        } finally {
            setLoading(false);
        }
    });

    /**
     * Clear invalid styling on input
     */
    form.querySelectorAll("input").forEach((input) => {
        input.addEventListener("input", () => {
            input.classList.remove("invalid");
        });
    });

    /**
     * Reset UI on form clear
     */
    resetBtn.addEventListener("click", () => {
        form.querySelectorAll("input").forEach((input) => {
            input.classList.remove("invalid");
        });
        showPanel(placeholderState);
        setLoading(false);
    });

    /** Button ripple-style click feedback */
    predictBtn.addEventListener("mousedown", () => {
        if (!predictBtn.disabled) {
            predictBtn.style.transform = "scale(0.98)";
        }
    });

    predictBtn.addEventListener("mouseup", () => {
        predictBtn.style.transform = "";
    });
})();

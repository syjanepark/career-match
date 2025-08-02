// CareerMatch Frontend Configuration
const CONFIG = {
    // Backend API URL - Update this for different environments
    API_BASE_URL: "https://career-match-0pw6.onrender.com",
    
    // API Endpoints
    ENDPOINTS: {
        MATCH: "/match",
        HEALTH: "/"
    },
    
    // Request timeout in milliseconds
    TIMEOUT: 30000,
    
    // Local storage keys
    STORAGE_KEYS: {
        CAREER_MATCH_DATA: "careerMatchData"
    }
};

// Helper function to get full API URL
function getApiUrl(endpoint) {
    return CONFIG.API_BASE_URL + endpoint;
}

// Helper function to make API requests
async function makeApiRequest(endpoint, data = null, method = 'GET') {
    const url = getApiUrl(endpoint);
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        timeout: CONFIG.TIMEOUT
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, getApiUrl, makeApiRequest };
} 
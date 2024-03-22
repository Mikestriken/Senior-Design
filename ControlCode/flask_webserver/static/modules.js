// * Basic Fetch Function
export const fetchURL = async function (url) {
    try {
        // * Load this webpage subdirectory asynchronously so that we don't reload the page.
        const response = await fetch(url)

        // * Log the Response
        console.log('HTTP status code:', response.status);
    }
    catch(error) {
        // * Handle any errors that occurred during the fetch operation
        console.error('Error:', error);
    }
}
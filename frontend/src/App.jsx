import { useState, useEffect } from 'react';

// We will no longer use App.css because we are using TailwindCSS
// import './App.css'; 

const API_URL = 'http://localhost:8000';

function App() {
  const [threats, setThreats] = useState([]);
  const [indicator, setIndicator] = useState('');
  const [type, setType] = useState('');
  const [source, setSource] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch threats from the backend
  const fetchThreats = async (query = '') => {
    try {
      const url = query ? `${API_URL}/threats/?indicator=${query}` : `${API_URL}/threats/`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setThreats(data);
    } catch (error) {
      console.error("Failed to fetch threats:", error);
    }
  };

  // Fetch threats on component mount
  useEffect(() => {
    fetchThreats();
  }, []);

  // Handle form submission for new threats
  const handleSubmit = async (e) => {
    e.preventDefault();
    const newThreat = { indicator, type, source };

    try {
      const response = await fetch(`${API_URL}/threats/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newThreat),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Clear form and refresh threats list
      setIndicator('');
      setType('');
      setSource('');
      fetchThreats(); // Refresh with no query to show all threats
    } catch (error) {
      console.error("Failed to submit threat:", error);
    }
  };

  // Handle search submission
  const handleSearch = (e) => {
    e.preventDefault();
    fetchThreats(searchQuery);
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen font-sans">
      <div className="container mx-auto p-8">
        <h1 className="text-4xl font-bold mb-8 text-center text-blue-400">CyberNexus</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Left Column: Submission Form */}
          <div className="md:col-span-1 bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Submit a New Threat</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                className="w-full p-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="text"
                value={indicator}
                onChange={(e) => setIndicator(e.target.value)}
                placeholder="Indicator (e.g., IP, URL)"
                required
              />
              <input
                className="w-full p-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="text"
                value={type}
                onChange={(e) => setType(e.target.value)}
                placeholder="Threat Type (e.g., phishing)"
                required
              />
              <input
                className="w-full p-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="text"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="Source (e.g., user-report)"
                required
              />
              <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300">
                Submit
              </button>
            </form>
          </div>

          {/* Right Column: Threat Feed */}
          <div className="md:col-span-2 bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Threat Feed</h2>
            
            {/* Search Form */}
            <form onSubmit={handleSearch} className="flex gap-2 mb-4">
              <input
                className="flex-grow p-2 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by indicator..."
              />
              <button type="submit" className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition duration-300">
                Search
              </button>
            </form>

            <div className="space-y-4 overflow-y-auto max-h-[60vh]">
              {threats.length > 0 ? threats.map((threat, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded-md shadow">
                  <p className="text-lg font-mono break-all">{threat.indicator}</p>
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-sm text-blue-300 bg-blue-900 px-2 py-1 rounded-full">{threat.type}</span>
                    <em className="text-sm text-gray-400">{threat.source}</em>
                  </div>
                </div>
              )) : (
                <p className="text-gray-400 text-center">No threats found.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
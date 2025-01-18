
const backendBaseUrl = 'http://127.0.0.1:5000';


/*    LUKE'S VERSION 

// Function to handle GET requests
async function fetchPosts(startDate, endDate, platformName) {
  try {
      const response = await fetch(`/api/posts?startDate=${startDate}&endDate=${endDate}&platformName=${platformName}`);
      if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
      const data = await response.json();
      console.log("GET Response Data:", data);
      // Populate the data into the DOM
      populateTable(data);
  } catch (error) {
      console.error("Error during GET:", error);
  }
}


///////// DATABASE SECTION ///////

//send request to back end
async function sendPostsData(endpoint,json) {
  try {
      const jsonElement=JSON.stringify(json);
      const response = await fetch(`${backendBaseUrl}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: jsonElement, // Match backend parameters
      });
      // console.log("Payload being sent:", jsonElement);
      if (!response.ok) throw new Error(`Failed to send: ${response.status}`);
      const data = await response.json();
      // console.log("POST Response Data:", data);
      //populateTable(data); // Render the table with received data
      return data;

  } catch (error) {
      console.error("Error during POST:", error);
  }
}

// get timeframe for **database section**
async function getDFExample() {
  let endpoint;
  const startDate = document.getElementById('start-date-Table').value;
  const endDate = document.getElementById('end-date-Table').value;
  const platformName= document.getElementById(`platform-select`).value;
  const topic= document.getElementById(`topic-select`).value;
  const limit=10;
  const realtime=true;

  

  if (!validateDates(startDate, endDate)) return;
  if(!platformName) return;
  if(!topic) return;

  
  if(realtime){
    switch(platformName){
      case 'YouTube':
        endpoint = '/api/youtube_comments';
        break;
        case 'Reddit':
          endpoint = '/api/reddit_posts';
          
          break;
          case 'Bluesky':
            endpoint = '/api/bsky_posts';
            
            break;
            default:
              alert('Invalid platform selection.');
              return;
            }
  }
  else{
      endpoint = '/api/query_posts';
  }



  let data= await sendPostsData(endpoint,{ start_date: startDate, end_date: endDate, platforms: platformName,topic:topic,limit:limit}); 


  populateTable(data);

}

//only for **database section**
async function populateTable(data) {
  const table = document.getElementById('dffetchExample');
  table.innerHTML = ''; 

  if (data.length === 0) {
    table.innerHTML = '<tr><td colspan="10">No results found for the selected timeframe.</td></tr>';
    return;
  }

  // Create table headers
  const headers = Object.keys(data[0]);
  const headerRow = `<tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
  table.innerHTML += headerRow;

  const maxRows = 5;
  const rowsToDisplay = data.slice(0, maxRows);

  rowsToDisplay.forEach(row => {
    const rowHTML = `<tr>${headers.map(h => `<td>${row[h]}</td>`).join('')}</tr>`;
    table.innerHTML += rowHTML;
  });

  if (data.length > maxRows) {
    const footerRow = `<tr><td colspan="${headers.length}">Showing 10 of ${data.length} results.</td></tr>`;
    table.innerHTML += footerRow;
  }
}

**/

// Function to handle GET requests
async function fetchPosts(startDate, endDate, platformName) {
  try {
      const response = await fetch(`/api/posts?startDate=${startDate}&endDate=${endDate}&platformName=${platformName}`);
      if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
      const data = await response.json();
      console.log("GET Response Data:", data);
      // Populate the data into the DOM
      populateTable(data);
  } catch (error) {
      console.error("Error during GET:", error);
  }
}

///////// DATABASE SECTION ///////
//send request to back end
async function sendPostsData({ startDate, endDate }) {
  try {
      const response = await fetch(`${backendBaseUrl}/api/query_posts`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ start_date: startDate, end_date: endDate }), // Match backend parameters
          
      });
      console.log("Payload being sent:", JSON.stringify({ start_date: startDate, end_date: endDate }));
      if (!response.ok) throw new Error(`Failed to send: ${response.status}`);
      const data = await response.json();
      console.log("POST Response Data:", data);
      populateTable(data); // Render the table with received data
  } catch (error) {
      console.error("Error during POST:", error);
  }
}
// get timeframe for **database section**
function getDFExample() {
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  console.log("Start Date:", startDate);
  console.log("End Date:", endDate);
  if (!validateDates(startDate, endDate)) return;
  sendPostsData({ startDate, endDate }); 
}

//only for **database section**
function populateTable(data) {
  const table = document.getElementById('dffetchExample');
  table.innerHTML = ''; 
  if (data.length === 0) {
    table.innerHTML = '<tr><td colspan="20">No results found for the selected timeframe.</td></tr>';
    return;
  }
  // Create table headers
  const headers = Object.keys(data[0]);
  const headerRow = `<tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
  table.innerHTML += headerRow;
  const maxRows = 5;
  const rowsToDisplay = data.slice(0, maxRows);
  rowsToDisplay.forEach(row => {
    const rowHTML = `<tr>${headers.map(h => `<td>${row[h]}</td>`).join('')}</tr>`;
    table.innerHTML += rowHTML;
  });
  if (data.length > maxRows) {
    const footerRow = `<tr><td colspan="${headers.length}">Showing 10 of ${data.length} results.</td></tr>`;
    table.innerHTML += footerRow;
  }
}
//fetch topic in real time **database section**
// SELECT FIRST START-DATE, END-DATE, TOPIC AND THEN PLATFORM
async function handlePlatformChange() {
  const platform = document.getElementById('platform-select').value;
  const topic = document.getElementById('topic-select').value;
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  if (!startDate || !endDate) {
    alert("Please select both start and end dates.");
    return;
  }
  
  if (!topic) {
    alert("Please select a topic.");
    return;
  }
  
  if (!platform) {
      alert("Please select a platform.");
      return;
  }
  let endpoint = '';
  let payload = {};
  switch (platform) {
      case 'YouTube':
          endpoint = '/api/youtube_comments';
          payload = {
              topic: topic,
              start_date: startDate,
              end_date: endDate,
              //limit: 100,
          };
          break;
      case 'Reddit':
          endpoint = '/api/reddit_posts';
          const redditUrl = `https://www.reddit.com/r/${topic}/comments/abcdef/example_post/`; 
      
          // Prepare the payload for the backend
          payload = {
              url: redditUrl, 
              limit: 50,    
          };
      
          try {
              const response = await fetch(`${backendBaseUrl}${endpoint}`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(payload),
              });
      
              if (!response.ok) {
                  throw new Error(`Failed to fetch Reddit data: ${response.status}`);
              }
      
              const data = await response.json();
              console.log("Reddit Data:", data);
      
              populateTable(data);
          } catch (error) {
              console.error("Error fetching Reddit data:", error);
          }
          break;
      case 'Bluesky':
          endpoint = '/api/bsky_posts';
          payload = {
              topic: topic,
              start_date: startDate,
              end_date: endDate,
              limit: 100,
          };
          break;
      default:
          alert('Invalid platform selection.');
          return;
  }
  try {
      const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
      });
      if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
      }
      const data = await response.json();
      console.log(`${platform} Data:`, data);
      // Display the fetched data
      populateTable(data);
  } catch (error) {
      console.error(`Error fetching ${platform} data:`, error);
  }
}

function validateDates(startDate, endDate) {
  if (!startDate || !endDate) {
      alert("Please select both start and end dates.");
      return false;
  }
  if (new Date(startDate) > new Date(endDate)) {
      alert("Start date must be before or equal to the end date.");
      return false;
  }
  return true;
}



///////// SENTIMENT SECTION ///////////
let sentChartInstance;

// get timeframe for **sentiment section**
async function sentiment() {
  const startDate = document.getElementById('start-date-sentiment').value;
  const endDate = document.getElementById('end-date-sentiment').value;
  const topic = document.getElementById('topic-sentiment').value;
  const platformName = document.getElementById('platform-sentiment').value;
  // if (!validateDates(startDate, endDate)) return; 
  
  let data= await sendPostsData('/api/sentiment_analysis',{ start_date: startDate, end_date: endDate, platforms: platformName,topic:topic}); 
  console.log(data)


  const pos = data.filter((item, index,array) =>item.sentiment=="positive").map((item,index,array)=> (
    {x:new Date(item.Timestamp),y:item.PostContent}
  ));
  const neu = data.filter((item, index,array) =>item.sentiment=="neutral").map((item,index,array)=> (
    {x:new Date(item.Timestamp),y:item.PostContent}
  ));  
  const neg = data.filter((item, index,array) =>item.sentiment=="negative").map((item,index,array)=> (
    {x:new Date(item.Timestamp),y:item.PostContent}
  ));
  
  const sentChart= document.getElementById('sentimentalChart')
  if (sentChartInstance) {
    sentChartInstance.destroy();
  }
  // console.log(pos)
  // console.log(neu)
  // console.log(neg)
  sentChartInstance= new Chart(sentChart, {
      type: 'line',
      data:{
        datasets: [
              {
              label: 'Positive',
              data: pos,    
              fill: false,
              borderColor: 'rgb(10, 121, 19)',
              tension: 0.0,
              borderWidth: 3
            },
            {
              label: 'Neutral',
              data: neu,    
              fill: false,
              borderColor: 'rgb(87, 87, 87)',
              tension: 0.0,
              borderWidth: 3
            },
            {
              label: 'Negative',
              data: neg,    
              fill: false,
              borderColor: 'rgb(231, 44, 19)',
              tension: 0.0,
              borderWidth: 3
            }
        

      ]},
      options: {
        responsive: true,
        maintainAspectRatio: false,
        // spanGaps: true,
        plugins: {
          legend: {
            align: `center`,
    
            position:`right`,
            display: true,
            labels: {
              font:{size: 14},
              usePointStyle: true,
              pointStyle: `line`
              // color: 'rgb(255, 99, 132)'
            }
          },tooltip: {
            mode: 'nearest',
            intersect: false
          },
          
          title: {
            text: `Sentiment Analysis`,
            display: true,
            align:`start`,
            font:{size: 20},
            padding: {
              top: 0,
              bottom: 10
          }
          },
          subtitle: {
            display: true,
            text: 'Positive, Neutral and Negative Distribution',
            align:`start`,
            font:{size: 14},
            padding: {
              top: 0,
              bottom: 10,
    
          }
        }
      },
      scales: {
        y: {
          title:{
            display:true,
            text: `Number of Mentions`,
            font:{size: 14},
          },
          stacked: false
        },
        x: {
          title:{
            display:true,
            text: `Time`,
            font:{size: 14},
          },
          type: 'time',
          time: {
            unit: 'day'
        },
        }
    
      } 
      }
    });

}

//*

sentChartInstance= new Chart(document.getElementById('sentimentalChart'), {
  type: 'line',
  data: {
    // labels: [`0`,`1`,`2`],
    datasets: [
      {
      label: 'Positive',
      data: [120, 150, 90],    
      fill: false,
      borderColor: 'rgb(10, 121, 19)',
      tension: 0.0,
      borderWidth: 3
    },
    {
      label: 'Neutral',
      data: [80, 110, 70],    
      fill: false,
      borderColor: 'rgb(87, 87, 87)',
      tension: 0.0,
      borderWidth: 3
    },
    {
      label: 'Negative',
      data: [40, 50, 30],    
      fill: false,
      borderColor: 'rgb(231, 44, 19)',
      tension: 0.0,
      borderWidth: 3
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        align: `center`,
        position:`right`,
        display: true,
        labels: {
          font:{size: 14},
          usePointStyle: true,
          pointStyle: `line`
          // color: 'rgb(255, 99, 132)'
        }
      },tooltip: {
        mode: 'nearest',
        intersect: false
      },
      
      title: {
        text: `Sentiment Analysis`,
        display: true,
        align:`start`,
        font:{size: 20},
        padding: {
          top: 0,
          bottom: 10
      }
      },
      subtitle: {
        display: true,
        text: 'Positive, Neutral and Negative Distribution',
        align:`start`,
        font:{size: 14},
        padding: {
          top: 0,
          bottom: 10,
      }
    }
  },
  scales: {
    y: {
      title:{
        display:true,
        text: `Number of Mentions`,
        font:{size: 14},
      }
    },
    x: {
      title:{
        display:true,
        text: `Time`,
        font:{size: 14},
        
      }
    }
  } 
  }
});
//*/
function sentimenatlAnalisis(){
  let startDate= document.querySelectorAll(`#sentiment > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#sentiment > .calendar > input`)[1].value;
  let topic= document.querySelectorAll(`#sentiment > .data-controls > select`)[0].value;
  let platformName= document.querySelectorAll(`#sentiment > .data-controls > select`)[1].value;
  // console.log("sent"+startDate);
  // console.log("sent"+endDate);
  // console.log("sent"+drop1);
  // console.log("sent"+drop2);
  sendPostsData({startDate,endDate,topic,platformName});

}


////////////// TOPIC MODELLING SECTION ////////////
//get timeframe for **topic modelling section**

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault(); 
  const fileInput = document.getElementById("csvFile");
  if (fileInput.files.length === 0) {
    alert("Please choose a file to upload.");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  try {
    document.getElementById("topicsParent").innerHTML = '<p>Processing... Please wait.</p>';
    const response = await fetch("http://localhost:5000/process_csv", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      const errorData = await response.json();
      alert(`Error: ${errorData.error}`);
      return;
    }
    const data = await response.json();
    console.log("Data received from backend:", data);
    if (data.error) {
      alert(`Error: ${data.error}`);
    } else {
      renderTopicsChart(data.topics, data.sizes, data.keywords);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while processing the file.");
  }
});


function renderTopicsChart(topics, sizes, keywords) {
  const topicsParent = document.getElementById("topicsParent");
  topicsParent.innerHTML = '<canvas id="topicsChart"></canvas>';
  const canvas = document.getElementById("topicsChart");
  canvas.style.width = "150%"; 
  canvas.style.height = "500px"; 
  // Check if topics are empty
  if (topics.length === 0) {
    topicsParent.innerHTML = '<p>No topics were generated. Please check the input data.</p>';
    return;
  }
  const totalSize = sizes.reduce((acc, size) => acc + size, 0);
  const percentages = sizes.map(size => ((size / totalSize) * 100).toFixed(2));
  const labelsWithPercentages = topics.map((topic, index) => `${topic} (${percentages[index]}%)`);
  const ctx = document.getElementById("topicsChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labelsWithPercentages, 
      datasets: [
        {
          label: "Number of Comments",
          data: sizes,
          backgroundColor: "rgba(194, 132, 220, 0.64)",
          borderColor: "rgb(158, 8, 245)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      indexAxis: "y", 
      plugins: {
        tooltip: {
          callbacks: {
            afterBody: function (tooltipItems) {
              const topicIndex = tooltipItems[0].dataIndex;
              const keywordsForTopic = keywords[topicIndex].slice(0, 5).join(", ");
              return `Keywords: ${keywordsForTopic}`;
            },
          },
        },
      },
      scales: {
        y: { 
          beginAtZero: true, 
          title: { display: true, text: "Number of Comments" },
        },
        x: { 
          title: { display: true, text: "Topics" },
        },
      },
    },
  });
}
function getRandomColor() {
  const r = Math.floor(Math.random() * 255);
  const g = Math.floor(Math.random() * 255);
  const b = Math.floor(Math.random() * 255);
  return `rgba(${r}, ${g}, ${b}, 0.9)`;
}
function renderPlaceholderChart() {
  const topicsParent = document.getElementById("topicsParent");
  // Clear any existing content
  topicsParent.innerHTML = '<canvas id="topicsChart"></canvas>';
  const ctx = document.getElementById("topicsChart").getContext("2d");
  // Placeholder data
  const placeholderTopics = ["Topic A", "Topic B", "Topic C", "Topic D"];
  const placeholderSizes = [0, 0, 0, 0];
  const placeholderKeywords = [
    ["Placeholder1", "Placeholder2", "Placeholder3"],
    ["Placeholder4", "Placeholder5", "Placeholder6"],
    ["Placeholder7", "Placeholder8", "Placeholder9"],
  ];
  // Render the placeholder chart
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: placeholderTopics,
      datasets: [
        {
          label: "Data",
          data: placeholderSizes,
          backgroundColor: "rgba(194, 132, 220, 0.64)",
          borderColor: "rgb(158, 8, 245)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      resonsive:true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            afterBody: function (tooltipItems) {
              const topicIndex = tooltipItems[0].dataIndex;
              const keywordsForTopic = placeholderKeywords[topicIndex]
                .join(", ");
              return `Keywords: ${keywordsForTopic}`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Data",
          },
        },
        x: {
          title: {
            display: true,
            text: "Topics",
          },
        },
      },
    },
  });
}
renderPlaceholderChart();


////////// TOP TOPICS SECTION //////////////

function validateDates(startDate, endDate) {
  if (!startDate || !endDate) {
      alert("Please select both start and end dates.");
      return false;
  }
  if (new Date(startDate) > new Date(endDate)) {
      alert("Start date must be before or equal to the end date.");
      return false;
  }
  return true;
}

//get timeframe for **top topics section**
function getDFExampleT() {
  const startDate = document.getElementById('start-date-trends').value;
  const endDate = document.getElementById('end-date-trends').value;
  if (!validateDates(startDate, endDate)) return; 
  sendPostsDataT({ startDate, endDate }); 
}
async function sendPostsDataT({ startDate, endDate }) {
  try {
      const response = await fetch(`${backendBaseUrl}/api/query_posts`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ start_date: startDate, end_date: endDate }), 
          
      });
      console.log("Payload being sent:", JSON.stringify({ start_date: startDate, end_date: endDate }));
      if (!response.ok) throw new Error(`Failed to send: ${response.status}`);
      const data = await response.json();
      console.log("POST Response Data:", data);
      return data; // Render the table with received data
  } catch (error) {
      console.error("Error during POST:", error);
  }
}
// Main function to handle the complete process
async function getTrendAnalysis() {
  const startDate = document.getElementById('start-date-trends').value;
  const endDate = document.getElementById('end-date-trends').value;
  const topic = document.getElementById('topicM').value;
  if (!validateDates(startDate, endDate)) {
      alert("Please select a valid timeframe.");
      return;
  }
  if (!topic) {
      alert("Please select a topic.");
      return;
  }
  try {
      const posts = await sendPostsDataT({ startDate, endDate });
      
      await analyzeTrends({ data: posts, topics: [topic], startDate, endDate });
  } catch (error) {
      console.error("Error during fetch or analysis:", error);
  }
}

// Function to perform trend analysis using the fetched posts and selected topic
async function analyzeTrends({ data, topics, startDate, endDate }) {
  try {
      const response = await fetch(`${backendBaseUrl}/api/trend_analysis`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
              data: data,
              topics: topics,
              start_date: startDate,
              end_date: endDate,
          }),
      });
      if (!response.ok) throw new Error(`Failed trend analysis: ${response.status}`);
      const result = await response.json();
      console.log("Trend Analysis Result:", result);
      // Update the chart with the analysis result
      populateTrendChart(result);
  } catch (error) {
      console.error("Error performing trend analysis:", error);
      throw error;
  }
}
// Global variable to store the chart instance
let trendsChartInstance;

function populateTrendChart(data) {
  const monthlyCounts = data.monthly_counts || [];
  if (monthlyCounts.length === 0) {
      alert("No trend data available for the selected timeframe.");
      return;
  }
  // Extract months and totals for each topic
  const labels = monthlyCounts.map(entry => entry.Month); // Assuming `Month` field
  const topics = Object.keys(monthlyCounts[0]).filter(key => key !== 'Month'); // Dynamically extract topic columns
  // Prepare datasets for each topic
  const datasets = topics.map((topic, index) => ({
      label: topic,
      data: monthlyCounts.map(entry => entry[topic] || 0), // Fill 0 for missing data
      borderWidth: 1,
      barPercentage: 0.8,
      categoryPercentage: 0.5,
      backgroundColor: [
          'rgb(68, 99, 255)',  // Color for Topic A
      ][index % 3],
  }));
  // Destroy existing chart instance if it exists
  const trendsChartElement = document.getElementById('trendsChart');
  if (trendsChartInstance) {
      trendsChartInstance.destroy();
  }
  trendsChartInstance = new Chart(trendsChartElement, {
      type: 'bar', 
      data: {
          labels: labels,
          datasets: datasets,
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'x', 
          plugins: {
              legend: {
                  align: 'center',
                  position: 'bottom',
                  display: true,
                  labels: {
                      font: { size: 14 },
                      borderRadius: 10,
                      usePointStyle: true,
                      pointStyle: 'circle',
                  },
              },
              title: {
                  text: 'Topic Frequency Across Platforms',
                  display: true,
                  align: 'middle',
                  font: { size: 20 },
                  padding: { top: 0, bottom: 5 },
              },
              subtitle: {
                  display: true,
                  text: 'Source: Predicto Platform',
                  align: 'center',
                  font: { size: 14 },
                  padding: { top: 0, bottom: 10 },
              },
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Month',
                      font: { size: 14 },
                  },
              },
              y: {
                  title: {
                      display: true,
                      text: 'Mentions',
                      font: { size: 14 },
                  },
                  beginAtZero: true,
              },
          },
      },
  });
}

async function getTopTopics() {
  const startDate = document.getElementById('start-date-trends').value;
  const endDate = document.getElementById('end-date-trends').value;
  if (!validateDates(startDate, endDate)) {
      alert("Please select a valid timeframe.");
      return;
  }
  try {
      const posts = await sendPostsDataT({ startDate, endDate });
      const response = await fetch(`${backendBaseUrl}/api/top_topics`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
              data: posts,
              column: 'PostContent', 
              start_date: startDate,
              end_date: endDate,
              top_n: 10, 
          }),
      });
      if (!response.ok) throw new Error(`Failed to fetch top topics: ${response.status}`);
      const topTopics = await response.json();
      console.log("Top Topics Data:", topTopics);
      updateChartWithTopTopics(topTopics);
  } catch (error) {
      console.error("Error fetching top topics:", error);
  }
}
function updateChartWithTopTopics(topTopics) {
  if (!topTopics || topTopics.length === 0) {
      alert("No data available for the top 10 topics.");
      return;
  }
  const labels = topTopics.map(topic => topic.Topic);
  const values = topTopics.map(topic => topic.Frequency);
  const backgroundColors = [
      'rgb(68, 99, 255)',  // Blue
      'rgb(79, 194, 79)',  // Green
      'rgb(255, 187, 99)', // Yellow-Orange
      'rgb(255, 99, 100)', // Red
      'rgb(255, 232, 103)', // Light Yellow
      'rgb(87, 87, 87)',   // Gray
      'rgb(128, 0, 255)',  // Purple
      'rgb(255, 99, 132)', // Pink
      'rgb(0, 191, 255)',  // Sky Blue
      'rgb(255, 165, 0)',  // Orange
  ];

  const dataset = {
      label: 'Frequency',
      data: values,
      borderWidth: 1,
      barPercentage: 0.8,
      categoryPercentage: 0.5,
      backgroundColor: labels.map((_, index) => backgroundColors[index % backgroundColors.length]),
  };
  // Destroy existing chart instance to avoid conflicts
  const trendsChartElement = document.getElementById('trendsChart');
  if (trendsChartInstance) {
      trendsChartInstance.destroy();
  }
  // Create a new chart instance
  trendsChartInstance = new Chart(trendsChartElement, {
      type: 'bar', 
      data: {
          labels: labels,
          datasets: [dataset],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'x', 
          plugins: {
              legend: {
                  align: 'center',
                  position: 'bottom',
                  display: true,
                  labels: {
                      font: { size: 14 },
                      borderRadius: 10,
                      usePointStyle: true,
                      pointStyle: 'circle',
                  },
              },
              title: {
                  text: 'Top 10 Topics',
                  display: true,
                  align: 'middle',
                  font: { size: 20 },
                  padding: { top: 0, bottom: 5 },
              },
              subtitle: {
                  display: true,
                  text: 'Source: Predicto Platform',
                  align: 'center',
                  font: { size: 14 },
                  padding: { top: 0, bottom: 10 },
              },
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Topics',
                      font: { size: 14 },
                  },
              },
              y: {
                  title: {
                      display: true,
                      text: 'Frequency',
                      font: { size: 14 },
                  },
                  beginAtZero: true,
              },
          },
      },
  });
}
// just a placeholder chart until it gets updated
function initializeChart() {
  const trendsChartElement = document.getElementById('trendsChart');
  const placeholderLabels = [''];
  const placeholderValues = [0];
  const dataset = {
      label: 'Frequency',
      data: placeholderValues,
      borderWidth: 1,
      barPercentage: 0.8,
      categoryPercentage: 0.5,
      backgroundColor: ['rgba(200, 200, 200, 0.5)'], 
  };
  trendsChartInstance = new Chart(trendsChartElement, {
      type: 'bar',
      data: {
          labels: placeholderLabels,
          datasets: [dataset],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
              legend: { display: false },
              title: {
                  display: true,
                  text: '',
              },
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Topics',
                  },
              },
              y: {
                  title: {
                      display: true,
                      text: 'Frequency',
                  },
                  beginAtZero: true,
              },
          },
      },
  });
}
initializeChart();


function validateDates(startDate, endDate) {
  if (!startDate || !endDate) {
      alert("Please select both start and end dates.");
      return false;
  }
  if (new Date(startDate) > new Date(endDate)) {
      alert("Start date must be before or equal to the end date.");
      return false;
  }
  return true;
}


// NEWS API SECTION
document.getElementById("newsUploadForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const fileInput = document.getElementById("newsCsvFile");
  const file = fileInput.files[0];
  if (!file) {
      alert("Please select a file to upload.");
      return;
  }
  const formData = new FormData();
  formData.append("file", file);
  try {
      const response = await fetch("http://127.0.0.1:5000/recommend_news", {
          method: "POST",
          body: formData,
      });
      const data = await response.json();
      if (response.ok) {
          console.log("Recommendations received:", data.recommendations);
          // populate the recommendations into a table
          populateNewsTable(data.recommendations);
      } else {
          console.error("Error fetching recommendations:", data.error);
          alert(data.error);
      }
  } catch (error) {
      console.error("An error occurred:", error);
      alert("An unexpected error occurred while fetching recommendations.");
  }
});
function populateNewsTable(recommendations) {
  const table = document.getElementById("newsResultsTable");
  table.innerHTML = ""; // Clear the table before populating it
  if (Object.keys(recommendations).length === 0) {
    table.innerHTML = '<tr><td colspan="2">No recommendations available.</td></tr>';
    return;
  }
  // Add table headers
  const headerRow = `
      <tr>
          <th>Topic</th>
          <th>Recommended Articles</th>
      </tr>`;
  table.innerHTML += headerRow;
  // Loop through topics and URLs
  for (const [topic, urls] of Object.entries(recommendations)) {
    const articleLinks = urls
      .map(
        (url) => `<a href="${url}" target="_blank">${url}</a>`
      )
      .join("<br>");
    const rowHTML = `
          <tr>
              <td>${topic}</td>
              <td>${articleLinks}</td>
          </tr>`;
    table.innerHTML += rowHTML;
  }
}

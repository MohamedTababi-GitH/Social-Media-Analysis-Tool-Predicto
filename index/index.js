

// {"PostID":{"0":"XF_eQYvk53JyIiExNoILn8IwcjQ","1":"_JkM-WNiNk2uDeJZCPbr1BK2IcY","2":"duRTpQVxa1zqVTcxNvCIJd7fR74"},"Timestamp":{"0":"2024-12-28T10:59:08Z","1":"2024-12-28T09:11:46Z","2":"2024-12-28T05:34:14Z"},"PlatformName":{"0":"youtube","1":"youtube","2":"youtube"},"Username":{"0":"@sarmadhabibkhan3036","1":"@Zack-hv9cl","2":"@nomadicroadrat"},"PostContent":{"0":"I might be moving abroad for my studies next year. I'm gonna need these recipes","1":"Za\u2019atar is in the core of Palestinian cuisine","2":"Ah, the national dish of Finland. Slowly but surely the word is getting out."},"NumberOfComments":{"0":0,"1":0,"2":0},"NumberOfLikes":{"0":0,"1":0,"2":0},"videoid":{"0":"dDLRaiocb_k","1":"dDLRaiocb_k","2":"dDLRaiocb_k"},"SearchedTopic":{"0":"Food","1":"Food","2":"Food"},"NumberOfReposts":{"0":null,"1":null,"2":null},"URL":{"0":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k","1":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k","2":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k"}}
/*
{"PostID":
    {"0":"XF_eQYvk53JyIiExNoILn8IwcjQ","1":"_JkM-WNiNk2uDeJZCPbr1BK2IcY","2":"duRTpQVxa1zqVTcxNvCIJd7fR74"}
    ,"Timestamp":
    {"0":"2024-12-28T10:59:08Z","1":"2024-12-28T09:11:46Z","2":"2024-12-28T05:34:14Z"}
    ,"PlatformName":
    {"0":"youtube","1":"youtube","2":"youtube"}
    ,"Username":
    {"0":"@sarmadhabibkhan3036","1":"@Zack-hv9cl","2":"@nomadicroadrat"}
    ,"PostContent":
    {"0":"I might be moving abroad for my studies next year. I'm gonna need these recipes","1":"Za\u2019atar is in the core of Palestinian cuisine","2":"Ah, the national dish of Finland. Slowly but surely the word is getting out."}
    ,"NumberOfComments":
    {"0":0,"1":0,"2":0}
    ,"NumberOfLikes":
    {"0":0,"1":0,"2":0}
    ,"videoid":
    {"0":"dDLRaiocb_k","1":"dDLRaiocb_k","2":"dDLRaiocb_k"}
    ,"SearchedTopic":
    {"0":"Food","1":"Food","2":"Food"}
    ,"NumberOfReposts":
    {"0":null,"1":null,"2":null}
    ,"URL":
    {"0":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k","1":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k","2":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k"}}
*/

const backendBaseUrl = 'http://127.0.0.1:5000';


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
              limit: 10,    
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
              //start_date: startDate,
              //end_date: endDate,
              limit: 10,
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

// get timeframe for **sentiment section**
function getDFExampleS() {
  const startDate = document.getElementById('start-date-sentiment').value;
  const endDate = document.getElementById('end-date-sentiment').value;

  if (!validateDates(startDate, endDate)) return; 

  sendPostsDataS({ startDate, endDate });
}

//send request to back end
async function sendPostsDataS({ startDate, endDate }) {
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

      sentimenatlAnalisis(data); //here to be populated with the sentiment analysis function WE DO NOT HAVE IT YET
  } catch (error) {
      console.error("Error during POST:", error);
  }
}

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

//get timeframe for **topic modelling section**
function getDFExampleM() {
  const startDate = document.getElementById('start-date-model').value;
  const endDate = document.getElementById('end-date-model').value;

  if (!validateDates(startDate, endDate)) return; 

  sendPostsData({ startDate, endDate }); 
}


function topicModeling(){

  let startDate= document.querySelectorAll(`#topics > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#topics > .calendar > input`)[1].value;
  let topic= document.querySelectorAll(`#topics > .data-controls > select`)[0].value;
  let platformName= document.querySelectorAll(`#topics > .data-controls > select`)[1].value;
  // console.log("topic"+startDate);
  // console.log("topic"+endDate);

  sendPostsData({startDate,endDate,topic,platformName});
}

//get timeframe for **top topics section**
function getDFExampleT() {
  const startDate = document.getElementById('start-date-trends').value;
  const endDate = document.getElementById('end-date-trends').value;

  if (!validateDates(startDate, endDate)) return; 

  sendPostsData({ startDate, endDate }); 
}
function trends(){

  let startDate= document.querySelectorAll(`#trends > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#trends > .calendar > input`)[1].value;
  let platformName= document.querySelectorAll(`#trends > select`)[0].value;
  // console.log("trends"+startDate);
  // console.log("trends"+endDate);
  // console.log("trends"+drop1);
  sendPostsData({startDate,endDate,platformName});

}



    // console.timeEnd()




const sentChart = document.getElementById('sentimentalChart');

new Chart(sentChart, {
  type: 'line',
  data: {
    labels: [`0`,`1`,`2`],
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


const topicsChart = document.getElementById('topicsChart');

let words= ['Word1', 'Word2', 'Word3', 'Word4', 'Word5'];
let wordCount=[
[10, 8, 6, 4, 3],
[7, 5, 3, 2, 1],
[9, 6, 5, 3, 2],
[9, 6, 5, 3, 2],
[9, 6, 5, 3, 2]];

new Chart(topicsChart, {
  type: 'bar',
  fill: true,
  data: {
    labels: words,
    datasets: [{
      label: 'Politics',
      data: wordCount[0],
      borderWidth: 1,

      backgroundColor:'rgb(68, 99, 255)'
    },{
      label: 'Food',
      data: wordCount[1],
      borderWidth: 1,

      backgroundColor:'rgb(79, 194, 79)'
    },{
      label: 'Entertainment',
      data: wordCount[2],
      borderWidth: 1,
      backgroundColor:'rgb(255, 99, 100)'
    },{
      label: 'Technology',
      data: wordCount[3],
      borderWidth: 1,

      backgroundColor:'rgb(255, 232, 103)'
    },{
      label: 'Environment',
      data: wordCount[4],
      borderWidth: 1,

      backgroundColor:'rgb(255, 187, 0)'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: {
      align: `center`,


      
      // position:`chartArea`,
      position:`bottom`,
      display: true,
      labels: {
        font:{size: 14},
        // pointStyleWidth:12,
        // useBorderRadius: true,
        borderRadius: 10,
        usePointStyle: true,
        // dockInsidePlotArea: true,
			  // verticalAlign: "right",
			  // horizontalAlign: "right",
      pointStyle: `circle`
        // color: 'rgb(255, 99, 132)'
      }
    },

      title: {
        text: `Topic Modeling Analysis`,
        display: true,
        align:`middle`,
        font:{size: 20},
        padding: {top: 0,bottom: 5}

        
      }
  },
  scales: {
    y: {
      title:{
        display:true,
        text: `Top Words`,
        font:{size: 14},
      }
    },
    x: {

      title:{
        display:true,
        text: `Frequency`,
        font:{size: 14},
        align:`end`
      }
    }

  } 
  }
});



const trendsChart = document.getElementById('trendsChart');

let platforms= ['YouTube', 'Reddit', 'BlueSky'];
let mentions=[
[10, 8, 6],
[7, 5, 3],
[9, 6, 5]];

new Chart(trendsChart, {
  type: 'bar',
  fill: true,
  data: {
    labels: platforms,
    datasets: [{
      label: 'Topic A',
      data: mentions[0],
      borderWidth: 1,
      barPercentage:0.8,
      categoryPercentage:0.5,
      backgroundColor:'rgb(68, 99, 255)'
    },{
      label: 'Topic B',
      data: mentions[1],
      borderWidth: 1,
      barPercentage:0.8,
      categoryPercentage:0.5,
      backgroundColor:'rgb(79, 194, 79)'
    },{
      label: 'Topic C',
      data: mentions[2],
      borderWidth: 1,
      barPercentage:0.8,
      categoryPercentage:0.5,

      backgroundColor:'rgb(255, 187, 99)'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'x',
    plugins: {
      legend: {
      align: `center`,


      
      position:`bottom`,
      display: true,
      labels: {
        font:{size: 14},
        // pointStyleWidth:12,
        // useBorderRadius: true,
        borderRadius: 10,
        usePointStyle: true,
        			dockInsidePlotArea: true,
			verticalAlign: "center",
			horizontalAlign: "right",
      pointStyle: `circle`
        // color: 'rgb(255, 99, 132)'
      }
    },

      title: {
        text: `Topic Frequency Across Platforms`,
        display: true,
        align:`middle`,
        font:{size: 20},
        padding: {top: 0,bottom: 5}

        
      },subtitle: {
        display: true,
        text: 'Source: Predicto Platform',
        align:`center`,
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
        text: `Top Words`,
        font:{size: 14},
      }
    },
    x: {

      // title:{
      //   display:true,
      //   text: `Frequency`,
      //   font:{size: 14},
      //   align:`end`
      // }
    }

  } 
  }
});

/*

const ctx = document.getElementById('sentimentalChart');

new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
*/



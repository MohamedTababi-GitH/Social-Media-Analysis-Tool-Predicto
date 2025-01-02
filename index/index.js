

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

// Function to handle POST requests
async function sendPostsData(startDate, endDate, platformName) {
  try {
    console.log(JSON.stringify({ startDate, endDate, platformName }));
      const response = await fetch('/api/posts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ startDate, endDate, platformName }),
      });
      if (!response.ok) throw new Error(`Failed to send: ${response.status}`);
      const data = await response.json();
      console.log("POST Response Data:", data);
  } catch (error) {
      console.error("Error during POST:", error);
  }
}



function getDFExample(){

  // console.log("testing");
  
  
  let startDate= document.querySelectorAll(`#data > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#data > .calendar > input`)[1].value;
  let platformName= document.querySelectorAll(`#data > .data-controls > select`)[0].value;
  // console.log("data"+startDate);
  // console.log("data"+endDate);
  // console.log("data"+drop);
  sendPostsData(startDate,endDate,platformName);

  // console.log(JSON.stringify({ startDate, endDate, platformName }));
  // Perform GET and POST requests
  // fetchPosts(startDate, endDate, platformName);
  // sendPostsData(startDate, endDate, platformName);








  








  // resizeTo(startDate,endDate,drop)
  
  // sentimenatlAnalisis();
  // topicModeling();
  // trends();
  
  var jselements=
  [{"PostID":"nxCG4h_7h98ALtV9CjwtzgJSse8","Timestamp":"2024-12-28T20:47:55Z","PlatformName":"youtube","Username":"@meganchristinadunn","PostContent":"Made this tonight and it was delicious! Thanks for the inspiration!","NumberOfComments":0,"NumberOfLikes":0,"videoid":"dDLRaiocb_k","SearchedTopic":"Food","NumberOfReposts":null,"URL":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k"},{"PostID":"G9aIFIL26RjmVjL1jAcUzeDnNBQ","Timestamp":"2024-12-28T19:28:41Z","PlatformName":"youtube","Username":"@curlyninjaw.9489","PostContent":"I don\u2018t think eating chicken is healthy\u2026 more veggies please","NumberOfComments":0,"NumberOfLikes":0,"videoid":"dDLRaiocb_k","SearchedTopic":"Food","NumberOfReposts":null,"URL":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k"},{"PostID":"PpjRUI4O6UzHj0Fh0xk3thSBHg8","Timestamp":"2024-12-28T19:23:07Z","PlatformName":"youtube","Username":"@lazardan8389","PostContent":"The meal is fried in oil, not healthy","NumberOfComments":0,"NumberOfLikes":0,"videoid":"dDLRaiocb_k","SearchedTopic":"Food","NumberOfReposts":null,"URL":"https:\/\/www.youtube.com\/watch?v=dDLRaiocb_k"}];
  
      
  
      let keys=Object.keys(jselements[0]);
      // console.log(keys);
  
  
      // console.time()
      document.getElementById('dffetchExample').innerHTML = `
      <thead>
          ${keys.map(x => `<th>${x}</th>`).join('')}
      </thead>
      <tBody>
          ${jselements.map(x => `<tr>${keys.map(y=> `<td>${x[y]}</td>`).join(``)}</tr>`).join(``)}
      </tBody>
      `
  }


function sentimenatlAnalisis(){

  let startDate= document.querySelectorAll(`#sentiment > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#sentiment > .calendar > input`)[1].value;
  let drop1= document.querySelectorAll(`#sentiment > .data-controls > select`)[0].value;
  let drop2= document.querySelectorAll(`#sentiment > .data-controls > select`)[1].value;
  // console.log("sent"+startDate);
  // console.log("sent"+endDate);
  // console.log("sent"+drop1);
  // console.log("sent"+drop2);
}
function topicModeling(){

  let startDate= document.querySelectorAll(`#topics > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#topics > .calendar > input`)[1].value;

  // console.log("topic"+startDate);
  // console.log("topic"+endDate);

}

function trends(){

  let startDate= document.querySelectorAll(`#trends > .calendar > input`)[0].value;
  let endDate= document.querySelectorAll(`#trends > .calendar > input`)[1].value;
  let drop1= document.querySelectorAll(`#trends > select`)[0].value;
  // console.log("trends"+startDate);
  // console.log("trends"+endDate);
  // console.log("trends"+drop1);

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



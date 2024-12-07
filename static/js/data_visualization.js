// MUST IMPORT CHART.JS FOR THIS TO WORK!!!!

document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('myChart').getContext('2d');
  var average_airline_delays = document.getElementById('myChart').getAttribute('avgDelays');
  var airlines = document.getElementById('myChart').getAttribute('airlines');
  
  console.log(average_airline_delays);
  console.log(typeof average_airline_delays);
  console.log(airlines);
  console.log(typeof airlines);

  //average_airline_delays = JSON.parse(average_airline_delays);
  airlines = JSON.parse(airlines);

  average_airline_delays = average_airline_delays.slice(1,-1).split(',').map(Number);
  //airlines = airlines.slice(1,-1).split(', ');
  //airlines = airlines.map(label => label.replace(/"/g, ''));

  console.log(average_airline_delays);
  console.log(typeof average_airline_delays);
  console.log(airlines);
  console.log(typeof airlines);

  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: airlines,
      datasets: [{
        label: 'Average Delay (Minutes)',
        data: average_airline_delays,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: false,
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        chartAreaBorder: {
          borderColor: 'blue',
          borderWidth: 2,
          borderDash: [5, 5],
          borderDashOffset: 2,
        }
      }
    }
  });
});

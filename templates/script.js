document.addEventListener("DOMContentLoaded", function() {
  fetch('/getChartData')
  .then(response => response.json())
  .then(data => {
      var plotData = [{
          x: data.x,
          y: data.y,
          type: 'bar',
          marker: {
              color: 'rgb(0, 123, 255)'
          }
      }];

      var layout = {
          title: 'Assignment Grade Distribution',
          font: {size: 18},
          xaxis: {
              title: 'Grade',
          },
          yaxis: {
              title: 'Number of Students',
          },
          bargap: 0.05
      };

      Plotly.newPlot('gradeDistributionChart', plotData, layout);
  })
  .catch(error => console.error('Error fetching chart data:', error));
});

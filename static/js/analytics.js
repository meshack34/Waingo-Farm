/*=============================================================================
WAINGO FARM
ANALYTICS
=============================================================================*/

document.addEventListener("DOMContentLoaded", () => {

    if (typeof window.analyticsData === "undefined") {
        return;
    }

    initializeRevenueChart();
    initializeStatusChart();

});


/*=============================================================================
REVENUE CHART
=============================================================================*/

function initializeRevenueChart() {

    const canvas = document.getElementById("revenueChart");

    if (!canvas) return;

    new Chart(canvas, {

        type: "line",

        data: {

            labels: analyticsData.revenueLabels,

            datasets: [

                {

                    label: "Revenue (KSh)",

                    data: analyticsData.revenueData,

                    borderColor: "#2E7D32",

                    backgroundColor: "rgba(46,125,50,.10)",

                    fill: true,

                    tension: 0.35,

                    borderWidth: 3,

                    pointRadius: 5,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#2E7D32",

                    pointBorderColor: "#ffffff",

                    pointBorderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {

                intersect: false,

                mode: "index"

            },

            plugins: {

                legend: {

                    display: false

                },

                tooltip: {

                    callbacks: {

                        label(context) {

                            return "KSh " + Number(context.raw).toLocaleString();

                        }

                    }

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback(value) {

                            return "KSh " + Number(value).toLocaleString();

                        }

                    }

                }

            }

        }

    });

}


/*=============================================================================
ORDER STATUS CHART
=============================================================================*/

function initializeStatusChart() {

    const canvas = document.getElementById("statusChart");

    if (!canvas) return;

    new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: analyticsData.statusLabels,

            datasets: [

                {

                    data: analyticsData.statusData,

                    backgroundColor: [

                        "#F59E0B",
                        "#10B981",
                        "#3B82F6",
                        "#EF4444"

                    ],

                    borderWidth: 0,

                    hoverOffset: 10

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "68%",

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        padding: 20,

                        boxWidth: 14,

                        usePointStyle: true

                    }

                }

            }

        }

    });

}
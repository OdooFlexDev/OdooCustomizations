/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";
import {onWillStart, onMounted, useState, useRef, useEffect, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import { loadBundle } from "@web/core/assets";

export class DoCrmDashboard extends Component {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.action = useService("action");
        this.canvasRef = useRef('canvas');
        this.LeadByCampaign = useRef('campain_canvas')
        this.forCanvasRef = useRef('forcasted_canvas')

        this.state = useState({
            period:'year',
            total_leads: null,
            total_customer: null,
            active_customer:null,
            total_opportunity: null,
            exp_revenue: null,
            revenue: null,
            win_ratio: null,
            opportunity_ratio: null,
            upcoming_events: [],
            current_lang: [],
            charts: [],
            top_sales_person_revenue: [],
            monthly_sales: {},
            forcasted_sales:{},
            // forcasted_charts : []
        })
        onWillStart(async () => {
            await loadBundle("web.chartjs_lib")
            await this.fetch_crm_data();
            await this.UpcomingEvents();
            await this.TopSalesPersonRevenue();
        });

        useEffect(() => {
            if (this.state.charts.length > 0) {
                this.state.charts.forEach(chart => {
                    chart.destroy();
                });
            }
            this.get_monthly_sales();
            this.get_forcasted_sales();
            this.get_leads_by_campaign();
        }, () => []);

    }

    OnChangePeriods(){
        console.log("===period method===")
    }
    async get_leads_by_campaign() {
        var self = this;
        var ctx = this.LeadByCampaign.el.getContext('2d');
        const arrays = await this.orm.call('crm.lead', "get_lead_by_campaign", []);

        const data = {
          labels: arrays[1],
          datasets: [{
            label: 'Leads By Campaign',
            data: arrays[0],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(155, 20, 86)'
            ],
            hoverOffset: 4
          }]
        };
        const chart = new Chart(ctx, {
              type: 'doughnut',
              data: data,
        });
        if (!this.state.charts) {
            this.state.charts = [];
        }
        this.state.charts.push(chart);


    }

    async get_forcasted_sales() {
        const result = await this.orm.call('crm.lead', "get_forcasted_monthly_sales", []);
        this.state.forcasted_sales = result;
        this.renderMonthlyForcastedSalesChart();
    }

    renderMonthlyForcastedSalesChart() {
        const ctx = this.forCanvasRef.el.getContext('2d');
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        // Prepare the data for the chart
        const months = Object.keys(this.state.forcasted_sales).map(month => {
            const [year, monthNum] = month.split('-');
            return `${monthNames[parseInt(monthNum) - 1]} ${year}`; // Format: "Nov 2023"
        });
        const salesData = Object.values(this.state.forcasted_sales);

        // Create a gradient for the bars
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(75, 192, 192, 0.8)'); // Light blue
        gradient.addColorStop(1, 'rgba(75, 192, 192, 0.2)'); // Light green

        // Create a new chart
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: months,
                datasets: [{
                    label: 'Forecasted Monthly Sales',
                    data: salesData,
                    backgroundColor: gradient, // Use gradient for bars
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    borderRadius: 10, // Rounded corners for bars
                    hoverBackgroundColor: 'rgba(255, 99, 132, 0.8)', // Change color on hover
                    hoverBorderColor: 'rgba(255, 99, 132, 1)',
                    hoverBorderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#333', // Legend text color
                            font: {
                                size: 14,
                                weight: 'bold',
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        cornerRadius: 5,
                        padding: 10,
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false, // Hide x-axis grid lines
                        },
                        ticks: {
                            color: '#333', // X-axis text color
                            font: {
                                size: 12,
                                weight: 'bold',
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(200, 200, 200, 0.2)', // Light gray grid lines
                        },
                        ticks: {
                            color: '#333', // Y-axis text color
                            font: {
                                size: 12,
                                weight: 'bold',
                            },
                            callback: function (value) {
                                return '$' + value; // Add dollar sign to y-axis values
                            }
                        }
                    }
                }
            }
        });

        // Store the chart instance in the state for later cleanup
        if (!this.state.charts) {
            this.state.charts = [];
        }
        this.state.charts.push(chart);
    }

    async get_monthly_sales() {
        const result = await this.orm.call('crm.lead', "get_monthly_sales", []);
        this.state.monthly_sales = result;

        this.renderMonthlySalesChart();
    }


    renderMonthlySalesChart() {
        const ctx = this.canvasRef.el.getContext('2d');
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        // Prepare the data for the chart
        const months = Object.keys(this.state.monthly_sales).map(month => monthNames[parseInt(month) - 1]);
        const salesData = Object.values(this.state.monthly_sales);
        console.log("==salesData==", salesData, months);

        // Create a gradient for the bars
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(75, 192, 192, 0.8)'); // Light blue
        gradient.addColorStop(1, 'rgba(75, 192, 192, 0.2)'); // Light green

        // Create a new chart
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months,
                datasets: [{
                    label: 'Monthly Sales',
                    data: salesData,
                    backgroundColor: gradient, // Use gradient for bars
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    borderRadius: 10, // Rounded corners for bars
                    hoverBackgroundColor: 'rgba(255, 99, 132, 0.8)', // Change color on hover
                    hoverBorderColor: 'rgba(255, 99, 132, 1)',
                    hoverBorderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#333', // Legend text color
                            font: {
                                size: 14,
                                weight: 'bold',
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        cornerRadius: 5,
                        padding: 10,
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false, // Hide x-axis grid lines
                        },
                        ticks: {
                            color: '#333', // X-axis text color
                            font: {
                                size: 12,
                                weight: 'bold',
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(200, 200, 200, 0.2)', // Light gray grid lines
                        },
                        ticks: {
                            color: '#333', // Y-axis text color
                            font: {
                                size: 12,
                                weight: 'bold',
                            },
                            callback: function (value) {
                                return '$' + value; // Add dollar sign to y-axis values
                            }
                        }
                    }
                }
            }
        });

        // Store the chart instance in the state for later cleanup
        this.state.charts.push(chart);
    }
    
    async fetch_crm_data() {
        var self = this
        var result = await this.orm.call('crm.lead', "get_crm_data", [this.state.period])
        this.state.total_customer = result['total_customer']
        this.state.active_customer = result['active_customer']
        this.state.exp_revenue = result['expected_revenue']
        this.state.revenue = result['revenue']
        this.state.total_leads = result['total_leads']
        this.state.total_opportunity = result['total_opportunity']
        this.state.win_ratio = result['win_ratio']
        this.state.opportunity_ratio = result['opportunity_ratio']
    }

    async UpcomingEvents() {
        var result = await this.orm.call('crm.lead', "get_upcoming_events", [this.state.period])
        this.state.upcoming_events = result['event']
        this.state.current_lang = result['cur_lang']
    }

    async TopSalesPersonRevenue(){
        var result = await this.orm.call('crm.lead', "get_top_salesperson_revenue", [this.state.period])
        this.state.top_sales_person_revenue = result['top_revenue']
    }

	 onClickTotalCustomers(){
	 	console.log("==onClickTotalCustomers===Clicked")
	 }
	 onClickActiveCustomers(){
	 	console.log("==onClickActiveCustomers===Clicked")
	 }

	 onClickRevenue(){
	 	console.log("==Revenue===Clicked")
	 }

	 onClickExpRevenue(){
	 	console.log("==onClickExpRevenue===Clicked")
	 }

	 onClickLeads(){
	 	console.log("==onClickLeads===Clicked")
	 }

	 onClickOpportunity(){
	 	console.log("==onClickOpportunity===Clicked")
	 }

}


DoCrmDashboard.template = 'DoCrmDashboard'
registry.category("actions").add("do_crm_dashboard", DoCrmDashboard)

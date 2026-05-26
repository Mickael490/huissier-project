import { Component, OnInit } from '@angular/core';
import { ChartModule } from 'primeng/chart';
import { debounceTime, Subscription } from 'rxjs';
import { LayoutService } from '../../../layout/service/layout.service';

@Component({
    standalone: true,
    selector: 'app-revenue-stream-widget',
    imports: [ChartModule],
    template: `<div class="card mb-8!">
        <div class="font-semibold text-xl mb-4">Activité du cabinet</div>
        <p-chart type="bar" [data]="chartData" [options]="chartOptions" class="h-100" />
    </div>`
})
export class RevenueStreamWidget implements OnInit {
    chartData: any;
    chartOptions: any;
    subscription!: Subscription;

    constructor(public layoutService: LayoutService) {
        this.subscription = this.layoutService.configUpdate$.pipe(debounceTime(25)).subscribe(() => {
            this.initChart();
        });
    }

    ngOnInit() {
        this.initChart();
    }

    initChart() {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color');
        const borderColor = documentStyle.getPropertyValue('--surface-border');
        const textMutedColor = documentStyle.getPropertyValue('--text-color-secondary');

        this.chartData = {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
            datasets: [
                {
                    type: 'bar',
                    label: 'Dossiers',
                    backgroundColor: '#4f46e5',
                    data: [2, 4, 3, 5, 2, 6],
                    barThickness: 32
                },
                {
                    type: 'bar',
                    label: 'Paiements (K FCFA)',
                    backgroundColor: '#10b981',
                    data: [150, 200, 180, 250, 300, 220],
                    barThickness: 32
                },
                {
                    type: 'bar',
                    label: 'Clients',
                    backgroundColor: '#f97316',
                    data: [1, 2, 1, 3, 2, 4],
                    borderRadius: { topLeft: 8, topRight: 8 },
                    borderSkipped: false,
                    barThickness: 32
                }
            ]
        };

        this.chartOptions = {
            maintainAspectRatio: false,
            aspectRatio: 0.8,
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                x: {
                    stacked: true,
                    ticks: { color: textMutedColor },
                    grid: { color: 'transparent', borderColor: 'transparent' }
                },
                y: {
                    stacked: true,
                    ticks: { color: textMutedColor },
                    grid: { color: borderColor, borderColor: 'transparent', drawTicks: false }
                }
            }
        };
    }

    ngOnDestroy() {
        if (this.subscription) {
            this.subscription.unsubscribe();
        }
    }
}
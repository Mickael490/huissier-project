import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [RouterModule, ToastModule],
    providers: [MessageService],
    template: `
      <p-toast position="top-right"></p-toast>
      <router-outlet></router-outlet>
    `
})
export class AppComponent implements OnInit, OnDestroy {
    private listener: any;

    constructor(private messageService: MessageService) {}

    ngOnInit() {
        this.listener = (e: any) => {
            this.messageService.add(e.detail);
        };
        window.addEventListener('app-toast', this.listener);
    }

    ngOnDestroy() {
        window.removeEventListener('app-toast', this.listener);
    }
}

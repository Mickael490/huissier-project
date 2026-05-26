import { Component, OnInit, ViewChild, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { CheckboxModule } from 'primeng/checkbox';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService } from 'primeng/api';
import { Cabinet, CabinetCreate } from 'src/types/cabinet';
import { CabinetService } from 'src/services/cabinets/cabinetService';
import { PdfService } from 'src/services/pdf.service';

@Component({
  selector: 'app-cabinet',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, InputTextModule,
    ConfirmDialogModule, CheckboxModule, TagModule
  ],
  templateUrl: './cabinet-component.html',
  providers: [MessageService, ConfirmationService]
})
export class CabinetComponent implements OnInit {

  cabinets = signal<Cabinet[]>([]);
  cabinet: Partial<Cabinet> = {};
  selectedCabinets: Cabinet[] = [];
  cabinetDialog = false;
  detailsDialog = false;
  submitted = false;
  cabinetSelectionne: any = null;

  @ViewChild('dt') dt!: Table;

  constructor(
    private cabinetService: CabinetService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadCabinets();
  }

  loadCabinets(): void {
    this.cabinetService.getCabinets().subscribe({
      next: (data) => this.cabinets.set(data),
      error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Impossible de charger les cabinets' })
    });
  }

  openNew(): void {
    this.cabinet = { actif: true };
    this.submitted = false;
    this.cabinetDialog = true;
  }

  editCabinet(cabinet: Cabinet): void {
    this.cabinet = { ...cabinet };
    this.cabinetDialog = true;
  }

  voirDetails(cabinet: any): void {
    this.cabinetSelectionne = cabinet;
    this.detailsDialog = true;
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editCabinet(this.cabinetSelectionne);
  }

  hideDialog(): void {
    this.cabinetDialog = false;
    this.submitted = false;
  }

  saveCabinet(): void {
    this.submitted = true;
    if (!this.cabinet.nom?.trim() || !this.cabinet.adresse?.trim()) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires' });
      return;
    }
    if (this.cabinet.id) {
      this.cabinetService.updateCabinet(this.cabinet.id, this.cabinet).subscribe({
        next: () => {
          this.loadCabinets();
          this.messageService.add({ severity: 'success', summary: 'Succes', detail: 'Cabinet modifie' });
          this.cabinetDialog = false;
          this.cabinet = {};
        },
        error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Impossible de mettre a jour' })
      });
    } else {
      this.cabinetService.createCabinet(this.cabinet as CabinetCreate).subscribe({
        next: () => {
          this.loadCabinets();
          this.messageService.add({ severity: 'success', summary: 'Succes', detail: 'Cabinet cree' });
          this.cabinetDialog = false;
          this.cabinet = {};
        },
        error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Impossible de creer' })
      });
    }
  }

  deleteCabinet(cabinet: Cabinet): void {
    this.confirmationService.confirm({
      message: 'Supprimer le cabinet "' + cabinet.nom + '" ?',
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.cabinetService.deleteCabinet(cabinet.id).subscribe(() => {
          this.loadCabinets();
          this.messageService.add({ severity: 'success', summary: 'Supprime', detail: 'Cabinet supprime' });
        });
      }
    });
  }

  onGlobalFilter(table: Table, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  exportListePDF(): void {
    this.pdfService.exportCabinets(this.cabinets());
  }

  exportFicheCabinetPDF(): void {
    if (this.cabinetSelectionne) {
      this.pdfService.exportFicheCabinet(this.cabinetSelectionne);
    }
  }
}

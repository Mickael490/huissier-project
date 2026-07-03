import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { PaiementService } from '../../../core/services/paiement.service';

@Component({
  selector: 'app-recu-paiement',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recu-paiement.component.html',
  styleUrls: ['./recu-paiement.component.scss']
})
export class RecuPaiementComponent implements OnInit {
  paiement: any = null;

  constructor(
    private route: ActivatedRoute,
    private paiementService: PaiementService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.paiementService.getPaiementById(+id).subscribe({
        next: (data) => (this.paiement = data),
      });
    }
  }

  imprimer(): void {
    window.print();
  }
}

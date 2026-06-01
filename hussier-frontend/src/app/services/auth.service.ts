import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userRole = new BehaviorSubject<string>('');

  constructor() {
    const stored = localStorage.getItem('userRole');
    if (stored) this.userRole.next(stored);
  }

  setRole(role: string) {
    this.userRole.next(role);
    localStorage.setItem('userRole', role);
  }

  getRole() {
    return this.userRole.asObservable();
  }

  hasPermission(requiredRoles: string[]): boolean {
    return requiredRoles.includes(this.userRole.value);
  }
}

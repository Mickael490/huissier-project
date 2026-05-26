import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface AppConfig {
  theme?: string;
  colorScheme?: string;
  scale?: number;
  [key: string]: any;
}

@Injectable({
  providedIn: 'root'
})
export class LayoutService {
  private configUpdate = new Subject<AppConfig>();
  configUpdate$ = this.configUpdate.asObservable();

  private _config: AppConfig = {
    theme: 'lara-light-indigo',
    colorScheme: 'light',
    scale: 14
  };

  get config(): AppConfig {
    return this._config;
  }

  updateConfig(config: AppConfig) {
    this._config = { ...this._config, ...config };
    this.configUpdate.next(this._config);
  }
}
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActeComponent } from './acte.component';

describe('ActeComponent', () => {
  let component: ActeComponent;
  let fixture: ComponentFixture<ActeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ActeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

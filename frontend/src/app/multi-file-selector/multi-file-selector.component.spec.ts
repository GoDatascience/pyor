import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MultiFileSelectorComponent } from './multi-file-selector.component';

describe('MultiFileSelectorComponent', () => {
  let component: MultiFileSelectorComponent;
  let fixture: ComponentFixture<MultiFileSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MultiFileSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MultiFileSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

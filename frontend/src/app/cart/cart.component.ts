import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart/cart.service';
import { Router } from '@angular/router';
import { CommonModule, NgIf } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterModule } from '@angular/router';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css'],
  standalone: true,
  imports: [RouterLink, RouterModule, RouterLinkActive, NgIf, CommonModule]
})
export class CartComponent implements OnInit {
  items = this.cartService.getItems();

  constructor(
    private cartService: CartService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.items = this.cartService.getItems();
  }

  decrementQuantity(index: number): void {
    if (this.items[index].quantity > 1) {
      this.items[index].quantity--;
      this.cartService.updateItems(this.items);
    } else {
      this.removeItem(index);
    }
  }

  incrementQuantity(index: number): void {
    this.items[index].quantity++;
    this.cartService.updateItems(this.items);
  }

  removeItem(index: number): void {
    this.items.splice(index, 1);
    this.cartService.updateItems(this.items);
  }

  goToPayment(): void {
    this.router.navigate(['/payment']);
  }

  getTotal(): number {
    // Calcular el precio total sumando el precio de cada ítem multiplicado por su cantidad
    return this.items.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  }
}
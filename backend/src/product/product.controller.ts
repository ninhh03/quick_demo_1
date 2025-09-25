import { Controller, Get, Param } from '@nestjs/common';
import { ProductService } from './product.service';

@Controller('products')
export class ProductController {
  constructor(private readonly productService: ProductService) {}

  @Get()
  async getAll() {
    return this.productService.findAll();
  }

  @Get(':id')
  async getOne(@Param('id') id: string) {
    return this.productService.findOne(id);
  }
}

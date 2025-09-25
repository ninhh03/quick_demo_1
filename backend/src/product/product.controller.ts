import { Controller, Get, Param, Query } from '@nestjs/common';
import { ProductService } from './product.service';

@Controller('products')
export class ProductController {
  constructor(private readonly productService: ProductService) {}

  @Get()
  async getAll(
    @Query('search') search?: string,
    @Query('minPrice') minPrice?: string,
    @Query('maxPrice') maxPrice?: string,
    @Query('diaChi') diaChi?: string,
    @Query('minReviews') minReviews?: string,
    @Query('maxReviews') maxReviews?: string,
    @Query('page') page = '1',
    @Query('limit') limit = '10',
  ) {
    return this.productService.findAll({
      search,
      minPrice: minPrice ? parseInt(minPrice, 10) : undefined,
      maxPrice: maxPrice ? parseInt(maxPrice, 10) : undefined,
      diaChi,
      minReviews: minReviews ? parseInt(minReviews, 10) : undefined,
      maxReviews: maxReviews ? parseInt(maxReviews, 10) : undefined,
      page: parseInt(page, 10),
      limit: parseInt(limit, 10),
    });
  }

  @Get(':id')
  async getOne(@Param('id') id: string) {
    return this.productService.findOne(id);
  }
}

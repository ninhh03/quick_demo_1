import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ProductService {
  constructor(private prisma: PrismaService) {}

  // Hàm parse giá từ string "1.600.000 đ" → number 1600000
  private parsePrice(priceStr: string): number {
    if (!priceStr) return 0;
    const numStr = priceStr.replace(/\./g, '').replace(/\s?đ/, '');
    return parseInt(numStr, 10) || 0;
  }

  async findAll(params: {
    search?: string;
    minPrice?: number;
    maxPrice?: number;
    diaChi?: string;
    minReviews?: number;
    maxReviews?: number;
    page?: number;
    limit?: number;
  }) {
    const {
      search,
      minPrice,
      maxPrice,
      diaChi,
      minReviews,
      maxReviews,
      page = 1,
      limit = 10,
    } = params;

    const skip = (page - 1) * limit;

    const where: any = {};

    // Search theo tên sản phẩm
    if (search) {
      where.ten_san_pham = { contains: search, mode: 'insensitive' };
    }

    // Filter theo địa chỉ
    if (diaChi) {
      where.dia_chi = { contains: diaChi, mode: 'insensitive' };
    }

    // Filter theo số lượng đánh giá
    if (minReviews || maxReviews) {
      where.so_luong_danh_gia = {};
      if (minReviews) where.so_luong_danh_gia.gte = minReviews;
      if (maxReviews) where.so_luong_danh_gia.lte = maxReviews;
    }

    // Lấy tất cả sản phẩm theo các filter trên (chưa filter giá)
    const allItems = await this.prisma.product.findMany({ where });

    // Filter giá bằng JS
    let filteredItems = allItems;
    if (minPrice || maxPrice) {
      filteredItems = allItems.filter((item) => {
        const num = this.parsePrice(item.gia || '');
        if (minPrice && num < minPrice) return false;
        if (maxPrice && num > maxPrice) return false;
        return true;
      });
    }

    const total = filteredItems.length;

    // Pagination JS
    const paginatedItems = filteredItems.slice(skip, skip + limit);

    return {
      data: paginatedItems,
      pagination: {
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  async findOne(id: string) {
    return this.prisma.product.findUnique({ where: { id } });
  }
}

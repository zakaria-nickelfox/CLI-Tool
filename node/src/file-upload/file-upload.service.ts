import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class FileUploadService {
  private uploadDir: string;

  constructor(private configService: ConfigService) {
    this.uploadDir = this.configService.get('UPLOAD_DIR', './uploads');
    if (!fs.existsSync(this.uploadDir)) {
      fs.mkdirSync(this.uploadDir, { recursive: true });
    }
  }

  async uploadFile(file: any): Promise<{ filename: string; url: string }> {
    const fileExt = path.extname(file.originalname);
    const filename = `${uuidv4()}${fileExt}`;
    const filePath = path.join(this.uploadDir, filename);

    fs.writeFileSync(filePath, file.buffer);

    const baseUrl = this.configService.get('BASE_URL', 'http://localhost:3000');
    return {
      filename,
      url: `${baseUrl}/uploads/${filename}`,
    };
  }

  async uploadMultipleFiles(files: any[]): Promise<{ filename: string; url: string }[]> {
    return Promise.all(files.map(file => this.uploadFile(file)));
  }

  async deleteFile(filename: string): Promise<void> {
    const filePath = path.join(this.uploadDir, filename);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }
}
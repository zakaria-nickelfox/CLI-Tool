import { Controller, Post, UseInterceptors, UploadedFile, UploadedFiles, Delete, Param } from '@nestjs/common';
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';
import { FileUploadService } from './file-upload.service';

@Controller('upload')
export class UploadController {
  constructor(private fileUploadService: FileUploadService) {}

  @Post()
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: any) {
    return this.fileUploadService.uploadFile(file);
  }

  @Post('multiple')
  @UseInterceptors(FilesInterceptor('files'))
  async uploadMultiple(@UploadedFiles() files: any[]) {
    return this.fileUploadService.uploadMultipleFiles(files);
  }

  @Delete(':filename')
  async deleteFile(@Param('filename') filename: string) {
    await this.fileUploadService.deleteFile(filename);
    return { message: 'File deleted successfully' };
  }
}
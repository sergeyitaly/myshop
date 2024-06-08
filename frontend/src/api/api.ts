import axios from 'axios';
import { Product } from '../models/entities';

export const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

interface Collection {
  id: string;
  name: string;
  photo: string;
  category: string;
}

// interface Product {
//   id: string;
//   name: string;
//   photo: string;
//   price: number | string;
//   description: string;
// }

// Function to fetch collection name by ID
export async function getCollectionNameById(collectionId: string): Promise<Collection> {
  try {
    const response = await axios.get<Collection>(`${apiBaseUrl}/api/collection/${collectionId}/`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching collection: ' + error);
  }
}

// Function to fetch product name by ID
export async function getProductNameById(productId: string): Promise<Product> {
  try {
    console.log(apiBaseUrl);
    
    const response = await axios.get<Product>(`${apiBaseUrl}/api/product/${productId}/`);
    console.log(response.data);
    
    return response.data;
  } catch (error) {
    throw new Error('Error fetching product: ' + error);
  }
}

// Function to fetch all collections with pagination
export async function getCollections(page: number = 1): Promise<{ results: Collection[], totalPages: number }> {
  try {
    const response = await axios.get<{ results: Collection[], totalPages: number }>(`${apiBaseUrl}/api/collections/?page=${page}`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching collections: ' + error);
  }
}

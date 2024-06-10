import axios from 'axios';
import { Product } from '../models/entities';
import { ServerResponce } from '../models/server-responce';

export const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

interface Collection {
  id: string;
  name: string;
  photo: string;
  category: string;
}


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
export async function getProductNameById(productId: string | number): Promise<Product> {
  try {
    const response = await axios.get<Product>(`${apiBaseUrl}/api/product/${productId}/`);
    
    return response.data;
  } catch (error) {
    throw new Error('Error fetching product: ' + error);
  }
}

export async function getCollectionProducts(collectionId: string, page: number): Promise<ServerResponce<Product[]>> {
  try{
    const response = await axios.get<ServerResponce<Product[]>>(`${apiBaseUrl}/api/collection/${collectionId}/products/?page=${page}`);
    
    return response.data;
  }
  catch (error) {
    throw new Error('Error fetching product: ' + error);
  }
};


export async function getProducts(queryString?: string): Promise<Product[]> {
  try{
    const response = await axios.get<ServerResponce<Product[]>>(`${apiBaseUrl}/api/products/?${queryString}`);
    
    return response.data.results;
  }
  catch (error) {
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

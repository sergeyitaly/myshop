import axios from 'axios';
import { Collection, Product } from '../models/entities';
import { ServerResponce, ShortServerResponce } from '../models/server-responce';
import { queryString } from 'object-query-string'
import { CollectionFilter, CollectionProductFilter, ProductFilter } from '../models/filters';

export const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;


// Function to fetch collection name by ID
export async function getCollectionNameById(collectionId: number): Promise<Collection> {
  try {
    const response = await axios.get<Collection>(`${apiBaseUrl}/api/collection/${collectionId}/`);
    
    return response.data;
  } catch (error) {
    throw new Error('Error fetching collection: ' + error);
  }
}

export async function getCollectionsByFilter(collectionFilter: CollectionFilter): Promise<ShortServerResponce<Collection[]>> {
  try {
    const qs = collectionFilter ? queryString(collectionFilter) : ''
    const response = await axios.get<ShortServerResponce<Collection[]>>(`${apiBaseUrl}/api/collections/?${qs}`);
    
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

export async function getCollectionProducts(collectionId: number): Promise<ShortServerResponce<Product[]>>  {
  try{
    const response = await axios.get<ShortServerResponce<Product[]>>(`${apiBaseUrl}/api/collection/${collectionId}/products/`);

    return response.data;
  }

  catch (error) {
    throw new Error('Error fetching product: ' + error);
  }
}

export async function getCollectionProductsByFilter(collectionId: number, query: CollectionProductFilter): Promise<ServerResponce<Product[]>> {
  try{
    const qs = queryString(query)
    const response = await axios.get<ServerResponce<Product[]>>(`${apiBaseUrl}/api/collection/${collectionId}/products/?${qs}`);
    
    return response.data;
  }
  catch (error) {
    throw new Error('Error fetching product: ' + error);
  }
}


export async function getProducts(productFilter?: ProductFilter): Promise<Product[]> {
  try{
    const qs = productFilter ? queryString(productFilter) : ''
    const response = await axios.get<ServerResponce<Product[]>>(`${apiBaseUrl}/api/products/?${qs}`);
    
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

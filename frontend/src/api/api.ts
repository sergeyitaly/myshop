import axios from 'axios';
import { Collection, Product, TeamMember, Technology, Brand } from '../models/entities';
import { ServerResponce, ShortServerResponce } from '../models/server-responce';
import { queryString } from 'object-query-string'
import { CollectionFilter, CollectionProductFilter, ProductFilter } from '../models/filters';

export const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;


// Function to fetch collection name by ID
export async function getCollectionNameById(collectionId: number): Promise<Collection> {
  try {
    const response = await axios.get<Collection>(`${apiBaseUrl}/api/collections/${collectionId}/`);
    
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

// Function to fetch TeamMembers
export async function getTeamMembers(): Promise<TeamMember[]> {
  try {
    const response = await axios.get<TeamMember[]>(`${apiBaseUrl}/api/team/`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching team members: ' + error);
  }
}

// Function to fetch Technology
export async function getTechnologies(): Promise<Technology[]> {
  try {
    const response = await axios.get<Technology[]>(`${apiBaseUrl}/api/technology/`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching technologies: ' + error);
  }
}

// Function to fetch Brands
export async function getBrands(): Promise<Brand[]> {
  try {
    const response = await axios.get<Brand[]>(`${apiBaseUrl}/api/brand/`);
    return response.data;
  } catch (error) {
    throw new Error('Error fetching brands: ' + error);
  }
}

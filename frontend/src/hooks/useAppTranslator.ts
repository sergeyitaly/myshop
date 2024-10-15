import { useTranslation } from "react-i18next";
import { Category, Collection, Currency, Product } from "../models/entities";
import { useCallback } from "react";

export const useAppTranslator = () => {

    const { i18n, t } = useTranslation();

    const getCategoryName = (category: Category): string => {
        switch (i18n.language) {
            case 'uk':
                return category.name_uk || category.name || '';
            case 'en':
                return category.name_en || category.name || '';
            default:
                return category.name_en || category.name || '';
        }
    };

    const getCollectionName = (collection: Collection): string => {
        switch (i18n.language) {
            case 'uk':
                return collection.name_uk || collection.name || '';
            case 'en':
                return collection.name_en || collection.name || '';
            default:
                return collection.name_en || collection.name || '';
        }
    };

    const getCurrencyFormat = (): Currency => {
        switch (i18n.language) {
            case 'uk':
                return 'UAH';
            case 'en':
                return 'USD';
            case 'fr':
                return 'EUR';
            default:
                return 'USD';
        }
    };

    const getTranslatedProductName = useCallback((product: Product): string => {
        return i18n.language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
      }, [i18n.language]);


    
 

    return {
        t,
        i18n,
        getCurrencyFormat,
        getCategoryName,
        getCollectionName,
        getTranslatedProductName
    }
}
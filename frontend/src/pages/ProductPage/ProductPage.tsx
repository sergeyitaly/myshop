import React from "react";
import { useParams } from "react-router-dom";
import { ProductSection } from "../../components/ProductSection/ProductSection";
import { MainContainer } from "./components/MainContainer";
import { useProduct } from "../../hooks/useProduct";
import { useGetCollectionByNameQuery } from "../../api/collectionSlice";
import { skipToken } from "@reduxjs/toolkit/query";
import { useTranslation } from "react-i18next";
import { FromThisCollectionSection } from "../../sections/FromThisCollectionSection/FromthisCollectionSection";
import { ProductPageSkeleton } from "./ProductPageSkeleton";


const ProductPage: React.FC = () => {
	const { id } = useParams<{ id: string }>();

	

	const { t } = useTranslation();

	const { product, isLoading, isFetching } = useProduct(id!);

	const collectionName = product?.collection?.name ?? skipToken;

	const { data: collection } = useGetCollectionByNameQuery(collectionName);


	return (
		<MainContainer >
			{
				isLoading ?
				<ProductPageSkeleton/>
				:
				product ?
				<>
					<ProductSection isLoading = {isFetching}/>
					<FromThisCollectionSection collectionId={collection?.id}/>
				</>
				:
				<div>{t("product_not_found")}</div>
			}
		</MainContainer>
	);
};

export default ProductPage;

import { useEffect, useState } from "react";
import { screens } from "../../../../constants";
import { useMediaQuery } from "@mui/material";
import ZoomIn from "@mui/icons-material/ZoomIn";
import { ProductImage } from "../../../../models/entities";
import { AppImage } from "../../../AppImage/AppImage";
import { Plug } from "../../../Plug/Plug";
import { transformURL } from "../../../../functions/transformURL";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import { AppModal } from "../../../AppModal/AppModal";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination } from "swiper/modules";
import styles from "./ProductGallery.module.scss";

interface ProductGalleryProps {
	smallImg?: string | null;
	defaultImage: string | null;
	images: ProductImage[];
	discount: boolean;
}

export const ProductGallery = ({
	defaultImage,
	smallImg,
	images,
	discount,
}: ProductGalleryProps) => {
	const isMobile = useMediaQuery(screens.maxMobile);

	const [currentImage, setCurrentImage] = useState<string | null>(
		defaultImage
	);
	const [open, setOpen] = useState<boolean>(false);

	useEffect(() => {
		setCurrentImage(defaultImage);
	}, [defaultImage]);

	const handleZoom = () => {
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};

	const swiperSettings = {
		spaceBetween: 10,
		slidesPerView: 1,
		pagination: {
			clickable: true,
		},
		loop: true,
		modules: [Pagination],
	};

	const handleClickZoomOnSlider = (src: string) => {
		setCurrentImage(src);
		setOpen(true);
	};

	return (
		<div className={styles.container}>
			{isMobile ? (
				<Swiper {...swiperSettings} className={styles.slider}>
					{images.map((image) => (
						<SwiperSlide
							key={image.id}
							className={styles.mobileImage}
						>
							<div className={styles.imageWrapper}>
								<AppImage
									src={image.images}
									previewSrc={smallImg}
									alt="product"
									onClick={() =>
										handleClickZoomOnSlider(image.images)
									}
								/>
								<button
									className={styles.zoomButton}
									onClick={() =>
										handleClickZoomOnSlider(image.images)
									}
								>
									<ZoomIn />
								</button>
							</div>
						</SwiperSlide>
					))}
				</Swiper>
			) : (
				<div className={styles.descktopMode}>
					<div className={styles.imageListContainer}>
						<div className={styles.imageList}>
							{images.map((image) => (
								<div
									key={image.id}
									className={styles.previevBox}
									onClick={() =>
										setCurrentImage(image.images)
									}
								>
									<AppImage
										src={image.images}
										previewSrc={image.images_thumbnail_url}
										alt="product"
									/>
								</div>
							))}
						</div>
					</div>
					<div className={styles.currentImageContainer}>
						<AppImage
							src={currentImage}
							previewSrc={smallImg}
							alt="product"
						/>
						<button
							className={styles.zoomButton}
							onClick={handleZoom}
						>
							<ZoomIn />
						</button>
						{discount && <Plug className={styles.plug} />}
					</div>
				</div>
			)}
			<AppModal open={open} onClickOutside={handleClose}>
				{currentImage ? (
					<TransformWrapper>
						<TransformComponent>
							<img src={transformURL(currentImage)} />
						</TransformComponent>
					</TransformWrapper>
				) : (
					<p>No image</p>
				)}
			</AppModal>
		</div>
	);
};

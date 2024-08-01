import { Modal, useMediaQuery } from '@mui/material'
import { screens } from '../../../../constants'
import { ProductImageSlider } from '../ProductImageSlider/ProductImageSlider'
import styles from './ProductGallery.module.scss'
import { useEffect, useState } from 'react'
import { ProductImage } from '../../../../models/entities'
import { AppImage } from '../../../AppImage/AppImage'
import ZoomIn from '@mui/icons-material/ZoomIn'
import { Plug } from '../../../Plug/Plug'
import { transformURL } from '../../../../functions/transformURL'

interface ProductGalleryProps {
    smallImg?: string | null
    defaultImage: string | null
    images: ProductImage[]
    discount: boolean
}

export const ProductGallery = ({
    defaultImage,
    smallImg,
    images,
    discount
}: ProductGalleryProps) => {

    const isMobile = useMediaQuery(screens.maxMobile)

    const [currentImage, setCurrentImage] = useState<string | null>(defaultImage)
    const [open, setOpen] = useState<boolean>(false)

    useEffect(() => {
        setCurrentImage(defaultImage)
    }, [defaultImage])


    const handleZoom = () => {
        setOpen(true)
    }

    const handleClose = () => {
        setOpen(false)
    }

    const handleClickZoomOnSlider = (src: string) => {
        setCurrentImage(src)
        setOpen(true)
    }

    return (
      <div className={styles.container}>
            {
                isMobile ?
                <ProductImageSlider
                    className={styles.imageBox}
                    discount={!!discount}
                    images={images}
                    onClickZoom={handleClickZoomOnSlider}
                    />
                :
                <div className={styles.descktopMode}>
                    <div className={styles.imageListContainer}>
                        <div className={styles.imageList}>
                            {
                                images.map((image) => (
                                <div 
                                    key={image.id}
                                    className={styles.previevBox}
                                    onClick={() => setCurrentImage(image.images)}
                                >
                                    <AppImage
                                        src={image.images}
                                        previewSrc={image.images_thumbnail_url}
                                        alt='product'
                                    />
                                </div>
                                ))
                            }
                        </div>
                    </div>
                    <div className={styles.currentImageContainer}>
                        <AppImage
                            src={currentImage}
                            previewSrc={smallImg}
                            alt='product'
                        />
                        <button
                            className={styles.zoomButton}
                            onClick={handleZoom}
                        >
                            <ZoomIn/>
                        </button>
                        {discount && 
                            <Plug className={styles.plug}/>
                        }
                    </div>
                </div>
            }
            <Modal
                open={open}
                onClose={handleClose}
            >
                {
                    currentImage ?
                    <img 
                        className={styles.modalContent}
                        src={transformURL(currentImage)}
                    />
                    :
                    <p>No image</p>
                }
            </Modal>
      </div>  
    )
}
import { useMediaQuery } from '@mui/material';
import { screens } from '../../../../constants';
import styles from './ProductGallery.module.scss'
import { MapComponent } from '../../../MapComponent';
import { Skeleton } from '../../../Skeleton/Skeleton';
import clsx from 'clsx';


export const ProductGellerySkeleton = () => {

    const isMobile = useMediaQuery(screens.maxMobile);



    return (
        <div className={styles.container}>
            {
                isMobile ?
                <Skeleton
                    className={clsx(styles.currentImageContainer, styles.current_image_skeleton)}
                />
                :
                <div className={styles.descktopMode}>
					<div className={styles.imageListContainer}>
						<div className={styles.imageList}>
							<MapComponent 
                                qty={3}
                                component={
                                    <Skeleton
                                        className={clsx(styles.previevBox, styles.previev_box_skeleton) }
                                    />
                                }
                            />
						</div>
					</div>
						<Skeleton
                            className={clsx(styles.currentImageContainer, styles.current_image_skeleton)}
                        />
				</div>
            }

        </div>
    )
}
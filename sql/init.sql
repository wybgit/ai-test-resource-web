-- AI Resources Database 初始化脚本
-- 基于原项目的数据库结构

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据集索引表
DROP TABLE IF EXISTS `dataset_index`;
CREATE TABLE `dataset_index` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `image_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_height` int NOT NULL,
  `image_width` int NOT NULL,
  `image_repository` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `bmp_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `yuv_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `json_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `positive_target` set('行人','车辆','建筑','动物','基础设施') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `negative_target` set('天空','植被','水面','路面','背景') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `target_distance` set('10m','15m','20m','25m','30m') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`image_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- 插入示例数据
INSERT INTO `dataset_index` VALUES 
(1, 'urban_road_001', 1080, 1920, 'urban_dataset', '/data/bmp/urban_road_001.bmp', '/data/yuv/urban_road_001.yuv', '/data/json/urban_road_001.json', '行人,车辆', '天空,路面', '10m,20m', 'road_camera'),
(2, 'wildlife_012', 720, 1280, 'wildlife_dataset', '/data/bmp/wildlife_012.bmp', '/data/yuv/wildlife_012.yuv', '/data/json/wildlife_012.json', '动物,基础设施', '植被,水面', '15m', 'wildlife_camera'),
(3, 'bridge_inspection_05', 512, 512, 'industrial_dataset', '/data/bmp/bridge_inspection_05.bmp', '/data/yuv/bridge_inspection_05.yuv', '/data/json/bridge_inspection_05.json', '建筑', '背景', '25m,30m', 'bridge_sensor'),
(4, 'highway_traffic_023', 1920, 1080, 'traffic_dataset', '/data/bmp/highway_traffic_023.bmp', '/data/yuv/highway_traffic_023.yuv', '/data/json/highway_traffic_023.json', '车辆,基础设施', '天空,路面', '20m,30m', 'highway_camera'),
(5, 'park_scene_007', 1280, 720, 'urban_dataset', '/data/bmp/park_scene_007.bmp', '/data/yuv/park_scene_007.yuv', '/data/json/park_scene_007.json', '行人,动物', '植被,背景', '10m,15m', 'park_camera');

-- 创建测试用例表
DROP TABLE IF EXISTS `test_cases`;
CREATE TABLE `test_cases` (
  `case_id` int NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `case_repository` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `case_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `case_json_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `category` enum('单算子','级联算子','block块','模型') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `label` set('depth fusion','fusion','M2M','tiling') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `framework` enum('onnx','caffe','ir') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `input_shape` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `model_size` decimal(10,2) NULL DEFAULT NULL COMMENT '模型大小(MB)',
  `params` bigint NULL DEFAULT NULL COMMENT '参数量',
  `flops` bigint NULL DEFAULT NULL COMMENT 'FLOPs',
  `sources` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`case_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- 插入示例数据
INSERT INTO `test_cases` VALUES 
(1, 'ResNet50_ImageNet', 'model_zoo', '/models/resnet50/resnet50.onnx', '/models/resnet50/config.json', '模型', 'fusion', 'onnx', '1x3x224x224', 97.8, 25557032, 4089184256, 'torchvision', NOW(), '经典图像分类模型'),
(2, 'YOLOv5s_Detection', 'detection_models', '/models/yolov5s/yolov5s.onnx', '/models/yolov5s/config.json', '模型', 'tiling', 'onnx', '1x3x640x640', 14.1, 7235389, 16500000000, 'ultralytics', NOW(), '轻量级目标检测模型'),
(3, 'Conv2D_Basic', 'operators', '/ops/conv2d/conv2d_basic.ir', '/ops/conv2d/config.json', '单算子', 'M2M', 'ir', '1x64x56x56', 0.5, 147456, 924844032, 'custom', NOW(), '基础卷积算子'),
(4, 'DepthFusion_Block', 'fusion_blocks', '/blocks/depth_fusion/depth_fusion.caffe', '/blocks/depth_fusion/config.json', 'block块', 'depth fusion,fusion', 'caffe', '1x128x28x28', 2.3, 589824, 1849688064, 'research', NOW(), '深度融合模块'),
(5, 'MobileNetV2_Cascade', 'mobile_models', '/models/mobilenetv2/cascade.onnx', '/models/mobilenetv2/config.json', '级联算子', 'tiling,fusion', 'onnx', '1x3x224x224', 13.4, 3504872, 300000000, 'torchvision', NOW(), '移动端优化模型');

SET FOREIGN_KEY_CHECKS = 1;
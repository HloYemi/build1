package com.kzjy.daedalus.client.model;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.minecraft.client.renderer.block.model.BlockModel;
import net.minecraft.client.renderer.block.model.ItemOverrides;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.Material;
import net.minecraft.client.resources.model.ModelBaker;
import net.minecraft.client.resources.model.ModelState;
import net.minecraft.client.resources.model.UnbakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.neoforged.neoforge.client.model.geometry.IGeometryBakingContext;
import net.neoforged.neoforge.client.model.geometry.IGeometryLoader;
import net.neoforged.neoforge.client.model.geometry.IUnbakedGeometry;

import java.util.Collections;
import java.util.function.Function;

public class DaedalusModelLoader implements IGeometryLoader<DaedalusModelLoader.DaedalusCosmicGeometry> {

    @Override
    public DaedalusCosmicGeometry read(JsonObject jsonObject, JsonDeserializationContext context) throws JsonParseException {
        JsonObject cosmicObj = jsonObject.getAsJsonObject("daedalus_cosmic");
        boolean isNeo = false;
        int neoType = 0;

        if (cosmicObj == null) {
            cosmicObj = jsonObject.getAsJsonObject("cosmic_neo");
            if (cosmicObj != null) {
                isNeo = true;
                neoType = GsonHelper.getAsInt(cosmicObj, "type", 0);
            }
        }

        if (cosmicObj == null) throw new IllegalStateException("Missing 'daedalus_cosmic' or 'cosmic_neo' object.");

        String maskPath = cosmicObj.get("mask").getAsString();
        JsonObject clean = jsonObject.deepCopy();
        clean.remove("daedalus_cosmic");
        clean.remove("cosmic_neo");
        clean.remove("loader");

        BlockModel baseModel = context.deserialize(clean, BlockModel.class);

        return new DaedalusCosmicGeometry(baseModel, ResourceLocation.parse(maskPath), isNeo, neoType);
    }

    public static class DaedalusCosmicGeometry implements IUnbakedGeometry<DaedalusCosmicGeometry> {
        private final BlockModel baseModel;
        private final ResourceLocation maskLocation;
        private final boolean isNeo;
        private final int neoType;

        public DaedalusCosmicGeometry(BlockModel baseModel, ResourceLocation maskLocation, boolean isNeo, int neoType) {
            this.baseModel = baseModel;
            this.maskLocation = maskLocation;
            this.isNeo = isNeo;
            this.neoType = neoType;
        }

        @Override
        public BakedModel bake(IGeometryBakingContext context, ModelBaker baker,
                               Function<Material, TextureAtlasSprite> spriteGetter,
                               ModelState modelState, ItemOverrides overrides) {
            BakedModel bakedBaseModel = this.baseModel.bake(baker, this.baseModel, spriteGetter, modelState, true);
            return new DaedalusCosmicBakedModel(bakedBaseModel, Collections.singletonList(maskLocation), isNeo, neoType);
        }

        @Override
        public void resolveParents(Function<ResourceLocation, UnbakedModel> modelGetter, IGeometryBakingContext context) {
            this.baseModel.resolveParents(modelGetter);
        }
    }
}
